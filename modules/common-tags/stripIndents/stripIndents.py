from createTag import createTag
from stripIndentTransformer import strip_indent_transformer
from trimResultTransformer import trim_result_transformer

stripIndents = createTag(strip_indent_transformer('all'), trim_result_transformer('smart'))