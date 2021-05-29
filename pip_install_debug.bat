set GLM_DIR="E:\GoodCode\glm-master"


set GLM_INCLUDE=-I%GLM_DIR%
py -3 -m pip install --global-option=build_ext --global-option=%GLM_INCLUDE% --global-option=--debug -v -e .
