from typing import List, Dict, Any, Union
import re

supportedTypes = ['initial', 'all']

def strip_indent_transformer(type: str = 'initial') -> Dict[str, Any]:
    if type not in supportedTypes:
        raise ValueError(f"Type not supported: {type}")

    def on_end_result(end_result: str) -> str:
        if type == 'all':
            # remove all indentation from each line
            return re.sub(r'^[^\S\n]+', '', end_result, flags=re.MULTILINE)
        else:
            # remove the shortest leading indentation from each line
            match = re.findall(r'^[^\S\n]*(?=\S)', end_result, flags=re.MULTILINE)
            indent = min(map(len, match), default=0) if match else 0
            if indent:
                regexp = re.compile(f'^.{{{indent}}}', flags=re.MULTILINE)
                return re.sub(regexp, '', end_result)
            return end_result

    return {'onEndResult': on_end_result}