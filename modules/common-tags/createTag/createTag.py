from utils.flat import flat

tagTransformersSymbol = 'COMMON_TAGS_TAG_TRANSFORMERS_SYMBOL'

def isTag(fn):
  return callable(fn) and hasattr(fn, tagTransformersSymbol)

def cleanTransformers(transformers):
  return flat([t[tagTransformersSymbol] if isTag(t) else t for t in transformers])

def getInterimTag(originalTag, extraTag):
  def tag(*args):
    return originalTag(['', ''], extraTag(*args))
  return tag

def getTagCallInfo(transformers):
  return {
    'transformers': transformers,
    'context': [t.getInitialContext() if hasattr(t, 'getInitialContext') else {} for t in transformers]
  }

def applyHook0(tagCallInfo, hookName, initialString):
  transformers, context = tagCallInfo['transformers'], tagCallInfo['context']
  for transformer, index in enumerate(transformers):
    if hasattr(transformer, hookName):
      initialString = transformer[hookName](initialString, context[index])
  return initialString

def applyHook1(tagCallInfo, hookName, initialString, arg1):
  transformers, context = tagCallInfo['transformers'], tagCallInfo['context']
  for transformer, index in enumerate(transformers):
    if hasattr(transformer, hookName):
      initialString = transformer[hookName](initialString, arg1, context[index])
  return initialString

def createTag(*rawTransformers):
  transformers = cleanTransformers(rawTransformers)

  def tag(strings, *expressions):
    nonlocal transformers
    if callable(strings):
      return getInterimTag(tag, strings)
    if not isinstance(strings, list):
      return tag([strings])

    tagCallInfo = getTagCallInfo(transformers)

    processedTemplate = ''.join([
      applyHook0(tagCallInfo, 'onString', string)
      for string in strings
    ])

    for index, expression in enumerate(expressions):
      processedTemplate += applyHook1(tagCallInfo, 'onSubstitution', expression, processedTemplate)
      processedTemplate += applyHook0(tagCallInfo, 'onString', strings[index+1])

    return applyHook0(tagCallInfo, 'onEndResult', processedTemplate)

  tag.__dict__[tagTransformersSymbol] = transformers
  return tag