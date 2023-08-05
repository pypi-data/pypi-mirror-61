from __future__ import print_function
import numpy
import logging

def laplace_kernel(k, v):
    kk = sum(ki ** 2 for ki in k)
    mask = (kk == 0).nonzero()
    kk[mask] = 1
    b = v / kk
    b[mask] = 0
    return b

def diff_kernel(dir, conjugate=False):
    def kernel(k, v):
        if conjugate:
            factor = -1j
        else:
            factor = 1j

        mask = (v.i[dir] != v.Nmesh[dir] // 2)
        return v * (factor * k[dir] * mask)
    return kernel

def create_grid(basepm, shift=0, dtype='f4'):
    """
        create uniform grid of particles, one per grid point on the basepm mesh

    """
    ndim = len(basepm.Nmesh)
    real = basepm.create('real')

    _shift = numpy.zeros(ndim, 'f8')
    _shift[:] = shift
    # one particle per base mesh point
    source = numpy.zeros((real.size, ndim), dtype=dtype)

    for d in range(len(real.shape)):
        real[...] = 0
        for xi, slab in zip(real.slabs.i, real.slabs):
            slab[...] = (xi[d] + 1.0 * _shift[d]) * (real.BoxSize[d] / real.Nmesh[d])
        source[..., d] = real.value.flat
    return source

def lpt1(dlin_k, q, resampler='cic'):
    """ Run first order LPT on linear density field, returns displacements of particles
        reading out at q. The result has the same dtype as q.
    """
    basepm = dlin_k.pm

    ndim = len(basepm.Nmesh)
    delta_k = basepm.create('complex')

    # only need to view the size
    delta_x = basepm.create('real', base=delta_k.base)

    layout = basepm.decompose(q)
    local_q = layout.exchange(q)

    source = numpy.zeros((delta_x.size, ndim), dtype=q.dtype)
    for d in range(len(basepm.Nmesh)):
        disp = dlin_k.apply(laplace_kernel) \
                    .apply(diff_kernel(d), out=Ellipsis) \
                    .c2r(out=Ellipsis)
        local_disp = disp.readout(local_q, resampler=resampler)
        source[..., d] = layout.gather(local_disp)
    return source

def lpt1_gradient(basepm, q, grad_disp, resampler='cic'):
    """ backtrace gradient of first order LPT on linear density field.
        returns gradient over modes of dlin_k. The positions are assumed to
        not to move, thus gradient over qition is not returned.

        The data partition of grad_disp must matchs the fastpm particle grid.
    """
    ndim = len(basepm.Nmesh)

    layout = basepm.decompose(q)
    local_q = layout.exchange(q)

    grad = basepm.create('complex')
    grad[...] = 0
    grad_disp_d = basepm.create('real')

    # for each dimension
    for d in range(ndim):
        local_grad_disp_d = layout.exchange(grad_disp[:, d])
        grad_disp_d.readout_gradient(local_q, local_grad_disp_d, resampler=resampler, out_self=grad_disp_d, out_pos=False)
        grad_delta_d_k = grad_disp_d.c2r_gradient(out=Ellipsis) \
                         .apply(laplace_kernel, out=Ellipsis) \
                         .apply(diff_kernel(d, conjugate=True), out=Ellipsis) \

        grad.value[...] += grad_delta_d_k.value

    # dlin_k are free modes in the compressed real FFT representation,
    # remember to take care of decompression later with decompress_gradient().
    # or better, always use RealField / WhiteNoise as free parameters.

    return grad

def lpt2source(dlin_k):
    """ Generate the second order LPT source term.  """
    source = dlin_k.pm.create('real')
    source[...] = 0
    D1 = [1, 2, 0]
    D2 = [2, 0, 1]

    phi_ii = []
    if dlin_k.ndim != 3:
        return source.r2c(out=Ellipsis)

    # diagnoal terms
    for d in range(dlin_k.ndim):
        phi_ii_d = dlin_k.apply(laplace_kernel) \
                     .apply(diff_kernel(d), out=Ellipsis) \
                     .apply(diff_kernel(d), out=Ellipsis) \
                     .c2r(out=Ellipsis)
        phi_ii.append(phi_ii_d)

    for d in range(3):
        source[...] += phi_ii[D1[d]].value * phi_ii[D2[d]].value

    # free memory
    phi_ii = []

    phi_ij = []
    # off-diag terms
    for d in range(dlin_k.ndim):
        phi_ij_d = dlin_k.apply(laplace_kernel) \
                 .apply(diff_kernel(D1[d]), out=Ellipsis) \
                 .apply(diff_kernel(D2[d]), out=Ellipsis) \
                 .c2r(out=Ellipsis)

        source[...] -= phi_ij_d[...] ** 2

    # this ensures x = x0 + dx1(t) + d2(t) for 2LPT

    source[...] *= 3.0 / 7
    return source.r2c(out=Ellipsis)

def lpt2source_gradient(dlin_k, grad_source):
    """ Generate the second order LPT source term.  """
    D1 = [1, 2, 0]
    D2 = [2, 0, 1]

    grad_dlin_k = dlin_k.copy()
    grad_dlin_k[...] = 0

    if dlin_k.ndim != 3:
        return grad_dlin_k

    grad_source_x = grad_source.r2c_gradient()

    grad_source_x[...] *= 3.0 / 7

    # diagonal terms, forward
    phi_ii = []
    for d in range(3):
        phi_ii_d = dlin_k.apply(laplace_kernel) \
                     .apply(diff_kernel(d), out=Ellipsis) \
                     .apply(diff_kernel(d), out=Ellipsis) \
                     .c2r(out=Ellipsis)
        phi_ii.append(phi_ii_d)

    # diagonal terms, backward
    for d in range(3):
        # every component is used twice, with D1 and D2
        grad_phi_ii_d = grad_source_x.copy()
        grad_phi_ii_d[...] *= (phi_ii[D1[d]].value + phi_ii[D2[d]].value)
        grad_dlin_k_d = grad_phi_ii_d.c2r_gradient(out=Ellipsis) \
                         .apply(diff_kernel(d, conjugate=True), out=Ellipsis) \
                         .apply(diff_kernel(d, conjugate=True), out=Ellipsis) \
                         .apply(laplace_kernel, out=Ellipsis)

        grad_dlin_k[...] += grad_dlin_k_d

    # off diagonal terms
    for d in range(3):
        # forward
        phi_ij_d = dlin_k.apply(laplace_kernel) \
                 .apply(diff_kernel(D1[d]), out=Ellipsis) \
                 .apply(diff_kernel(D2[d]), out=Ellipsis) \
                 .c2r(out=Ellipsis)

        # backward
        grad_phi_ij_d = phi_ij_d
        grad_phi_ij_d[...] *= -2 * grad_source_x[...]
        grad_dlin_k_d = grad_phi_ij_d.c2r_gradient(out=Ellipsis) \
                    .apply(diff_kernel(D2[d], conjugate=True), out=Ellipsis) \
                    .apply(diff_kernel(D1[d], conjugate=True), out=Ellipsis) \
                    .apply(laplace_kernel, out=Ellipsis)
        grad_dlin_k[...] += grad_dlin_k_d

    return grad_dlin_k

def gravity(x, pm, factor, f=None, return_deltak=False):
    field = pm.create(mode="real")
    layout = pm.decompose(x)
    field.paint(x, layout=layout, hold=False)

    deltak = field.r2c(out=Ellipsis)
    if f is None:
        f = numpy.empty_like(x)

    for d in range(field.ndim):
        force_d = deltak.apply(laplace_kernel) \
                  .apply(diff_kernel(d), out=Ellipsis) \
                  .c2r(out=Ellipsis)
        force_d.readout(x, layout=layout, out=f[..., d])
    f[...] *= factor

    if return_deltak:
        rho = deltak.c2r(out=Ellipsis)
        rho = rho.readout(x, layout=layout)
        return f, deltak, rho
    else:
        return f

def gravity_gradient(x, pm, factor, grad_f, out_x=None):
    if out_x is None:
        out_x = numpy.zeros_like(x)

    field = pm.create(mode="real")
    layout = pm.decompose(x)

    field.paint(x, layout=layout, hold=False)
    deltak = field.r2c(out=Ellipsis)
    grad_deltak = pm.create(mode="complex")
    grad_deltak[...] = 0

    for d in range(field.ndim):
        # forward
        force_d = deltak.apply(laplace_kernel) \
                  .apply(diff_kernel(d), out=Ellipsis) \
                  .c2r(out=Ellipsis)

        grad_force_d, grad_x_d = force_d.readout_gradient(
            x, btgrad=grad_f[:, d], layout=layout)

        grad_deltak_d = grad_force_d.c2r_gradient(out=Ellipsis) \
                        .apply(laplace_kernel, out=Ellipsis) \
                        .apply(diff_kernel(d, conjugate=True), out=Ellipsis) \
        grad_deltak[...] += grad_deltak_d
        out_x[...] += grad_x_d

    grad_field = grad_deltak.r2c_gradient(out=Ellipsis)
    grad_x, grad_mass = grad_field.paint_gradient(x, layout=layout, out_mass=False)
    out_x[...] += grad_x

    # should have been first applied to grad_f, but it is the same applying it here
    # and saves some memory
    out_x[...] *= factor

    return out_x

