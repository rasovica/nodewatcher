from nodewatcher.registry.cgm import base as cgm_base

def generate_config(node, only_validate = False):
  """
  Generates configuration and/or firmware for the specified node.
  
  @param node: Node instance
  @param only_validate: True if only validation should be performed
  """
  # Determine the destination platform
  try:
    platform = cgm_base.get_platform(node.config.core.general().platform)
  except (AttributeError, KeyError):
    return None
  
  cfg = platform.generate(node)
  if not only_validate:
    platform.defer_format_build(node, cfg)
  
  return cfg
