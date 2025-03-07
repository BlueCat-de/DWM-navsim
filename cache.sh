# 激活环境
source ~/miniconda3/bin/activate
conda init bash
conda activate /high_perf_store/surround-view/cqm/envs/diffusiondrive

# 设置环境变量
export NUPLAN_MAP_VERSION="nuplan-maps-v1.0"

export NUPLAN_MAPS_ROOT="/high_perf_store/surround-view/cqm/data/navsim/dataset/maps"

export NAVSIM_DEVKIT_ROOT="/high_perf_store/surround-view/cqm/projects/E2E/DWM-navsim"

export OPENSCENE_DATA_ROOT="/high_perf_store/surround-view/cqm/data/navsim/dataset"

export NAVSIM_EXP_ROOT="/high_perf_store/surround-view/cqm/projects/E2E/DWM-navsim/exp"


export PYTHONPATH=$PYTHONPATH:/high_perf_store/surround-view/cqm/projects/E2E/DWM-navsim

export PYTHONPATH=$PYTHONPATH:/high_perf_store/surround-view/cqm/projects/E2E/nuplan-devkit

export PYTHONPATH=$PYTHONPATH:/high_perf_store/surround-view/cqm/projects/E2E/nuplan-devkit/nuplan

export PYTHONPATH=$PYTHONPATH:/high_perf_store/surround-view/cqm/projects/E2E/DWM-navsim/

export PYTHONPATH=$PYTHONPATH:/high_perf_store/surround-view/cqm/projects/E2E/DWM-navsim/navsim/




python navsim/planning/script/run_dataset_caching.py \
    agent=DWM_agent \
    experiment_name=caching \
    train_test_split=navtrain \
