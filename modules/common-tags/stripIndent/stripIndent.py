from createTag import createTag
from stripIndentTransformer import strip_indent_transformer
from trimResultTransformer import trim_result_transformer

stripIndent = createTag(strip_indent_transformer(), trim_result_transformer('smart'))