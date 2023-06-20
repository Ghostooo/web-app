"""
MCAI Python Worker
Basic structure of a Media Cloud AI worker.
"""
from typing import Optional
import logging
import sys
import socket
import mcai_worker_sdk as mcai
from py_image_classification import classif_tasks

logger = logging.getLogger()


class McaiWorkerParameters(mcai.WorkerParameters):
    """
    Worker parameters class
    This class defines the input parameters of each job processed by the worker.
    They need to be explicitly typed to allow the SDK to type them properly when a job arrives.
    """

    source_path: str = None
    requirements: list = None
    destination_path: str = None
    inference_config: str = None
    threshold: float = 0.6



class McaiWorker(mcai.Worker):
    """
    Worker class
    This is the implementation of your worker. It includes several methods that can be optional.
    """
        
    def process(self, _handle_callback, _parameters: McaiWorkerParameters, job_id: int):
        """
        Standard worker process function.
        """
        log_level = os.environ.get('MCAI_LOG', 'info').upper()
        logging.basicConfig(stream=sys.stdout,
                            level=getattr(logging, log_level),
                            format="%(asctime)s.%(msecs)03d000000 UTC - {container_id:s} - {job_queue:s} - {jobid:d}  - %(levelname)s - %(message)s".format(
                                container_id=socket.gethostname(),
                                job_queue=os.getenv("AMQP_QUEUE", default="unknown_queue"),
                                jobid=job_id
                            ),
                            datefmt="%Y-%m-%d %H:%M:%S"
                            )

        classif_tasks.task_classif(_parameters.__dict__)
        _handle_callback.set_job_status(status=mcai.JobStatus.Completed)
    
    
def main():
    """
    This function must be defined. It will be the entrypoint of your worker
    """
    description = mcai.WorkerDescription(__package__)
    worker = McaiWorker(McaiWorkerParameters, description)
    worker.start()

if __name__ == "__main__":
    main()


