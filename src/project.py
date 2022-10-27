"""Define the project's workflow logic and operation functions.

Execute this script directly from the command line, to view your project's
status, execute operations and submit them to a cluster. See also:

    $ python src/project.py --help
"""
import signac
from flow import FlowProject, directives
from flow.environment import DefaultSlurmEnvironment
import os


class MyProject(FlowProject):
    pass


class Borah(DefaultSlurmEnvironment):
    hostname_pattern = "borah"
    template = "borah.sh"

    @classmethod
    def add_args(cls, parser):
        parser.add_argument(
            "--partition",
            default="gpu",
            help="Specify the partition to submit to."
        )


class R2(DefaultSlurmEnvironment):
    hostname_pattern = "r2"
    template = "r2.sh"

    @classmethod
    def add_args(cls, parser):
        parser.add_argument(
            "--partition",
            default="gpuq",
            help="Specify the partition to submit to."
        )


class Fry(DefaultSlurmEnvironment):
    hostname_pattern = "fry"
    template = "fry.sh"

    @classmethod
    def add_args(cls, parser):
        parser.add_argument(
            "--partition",
            default="batch",
            help="Specify the partition to submit to."
        )

# Definition of project-related labels (classification)
@MyProject.label
def sampled(job):
    return job.doc.get("done")


@MyProject.label
def initialized(job):
    return job.isfile("sim_traj.gsd")


@directives(executable="python -u")
@directives(ngpu=1)
@MyProject.operation
@MyProject.post(sampled)
def sample(job):
    from polyellipsoid import System, Simulation 
    from cmeutils.gsd_utils import ellipsoid_gsd

    with job:
        print("-----------------------")
        print("JOB ID NUMBER:")
        print(job.id)
        print("-----------------------")
        print()
        print("----------------------")
        print("Creating the system...")
        print("----------------------")
        print()
        system = System(
                n_chains=job.sp.n_chains,
                chain_lengths=job.sp.chain_lengths,
                bead_mass=job.sp.bead_mass,
                bead_length=job.sp.bead_length,
                bond_length=job.sp.bond_length,
                density=job.sp.density
        )
        print("----------------------")
        print("Creating the simulation...")
        print("----------------------")
        print()
        sim = Simulation(
                system,
                epsilon=job.sp.epsilon,
                lperp=job.sp.lperp,
                lpar=job.sp.lpar,
                tau=job.sp.tau_kt,
                dt=job.sp.dt,
                r_cut=job.sp.r_cut,
                bond_k=job.sp.bond_k
                angle_k=job.sp.angle_k,
                angle_theta=job.sp.angle_theta,
                seed=job.sp.sim_seed,
                gsd_write=int(job.doc.total_steps / job.sp.n_frames)
                log_write=int(job.doc.total_steps / job.sp.n_logs)
        )

    


if __name__ == "__main__":
    MyProject().main()
