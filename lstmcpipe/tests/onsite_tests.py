"""
Unit tests to run on the cluster
"""

import pytest
from pathlib import Path
import tempfile
import subprocess

from lstmcpipe.scripts import generate_test_lapalma
from lstmcpipe.scripts.lstmcpipe_generate_config import dump_lstchain_std_config


def not_running_in_lapalma():
    """
    Check if we are running on the cluster
    """
    return not Path("/fefs/aswg/data/mc").exists()


@pytest.mark.skipif(not_running_in_lapalma(), reason="Tests to run on the cluster")
@pytest.fixture
def prepare_tests_allsky():
    tmpdir_path = tempfile.mkdtemp()
    config_file_path_allsky = Path(tmpdir_path, f'test_AllSky.yaml')
    generate_test_lapalma.generate_test_allsky(working_dir=tmpdir_path,
                                               path_to_config_file=config_file_path_allsky
                                              )
    lstchain_cfg = Path(tmpdir_path, 'lstchain_config.json')
    dump_lstchain_std_config(filename=lstchain_cfg)
    
    
    return tmpdir_path, config_file_path_allsky, lstchain_cfg


@pytest.mark.skipif(not_running_in_lapalma(), reason="Tests to run on the cluster")
def test_r0_to_dl1(prepare_tests_allsky):
    tmpdir_path, config_file_path_allsky, lstchain_cfg = prepare_tests_allsky
    
    cmd = ['lstmcpipe', '-c', config_file_path_allsky, '-conf_lst', lstchain_cfg]
    subprocess.run(cmd)
    print(list(Path(tmpdir_path).iterdir()))

    