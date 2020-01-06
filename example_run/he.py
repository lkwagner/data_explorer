if __name__ == "__main__":
    import pyscf
    import pyqmc
    import pandas as pd
    import h5py
    import uuid
    import itertools

    mol = pyscf.gto.M(atom = "He 0. 0. 0.", basis='bfd_vdz', ecp='bfd', unit='bohr')

    mf = pyscf.scf.RHF(mol).run()

    for nconfig, steprange, npts in itertools.product([250, 500, 1000], [0.1, 0.2], [5, 10] ):
        nconfig = nconfig
        configs = pyqmc.initial_guess(mol, nconfig)
        wf = pyqmc.slater_jastrow(mol, mf)
        acc = pyqmc.gradient_generator(mol, wf, ['wf2acoeff','wf2bcoeff'])

        identity = str(uuid.uuid4())
        fname = f"../static/{identity}.hdf5"
        pyqmc.line_minimization(wf, configs, acc, hdf_file = fname, steprange = steprange, npts=npts)

        #These are not saved by line minimization, so we save them here.
        with h5py.File(fname) as f:
            f.attrs['uuid'] = identity
            f.attrs['nconfig'] = nconfig
