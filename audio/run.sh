CWD="$(dirname "$0")"
export LICORICE_MODEL_PATH="$(dirname "$0")"
export LICORICE_MODULE_PATH="$(dirname "$0")/modules"
export LICORICE_TEMPLATE_PATH="$(dirname "$0")/drivers"
licorice go lights_audio -y "$@"


# LICORICE_WORKING_PATH=$CWD LICORICE_TEMPLATE_PATH=$CWD/drivers licorice go lights_audio -y "$@"
