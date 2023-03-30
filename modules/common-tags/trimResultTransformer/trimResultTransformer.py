from typing import Dict, Any
import re

supportedSides = ['', 'start', 'left', 'end', 'right', 'smart']

def trim_result_transformer(side: str = '') -> Dict[str, Any]:
    if side not in supportedSides:
        raise ValueError(f"Side not supported: {side}")

    def on_end_result(end_result: str) -> str:
        if side == '':
            return end_result.strip()
        elif side in ['start', 'left']:
            return re.sub(r'^\s*', '', end_result)
        elif side in ['end', 'right']:
            return re.sub(r'\s*$', '', end_result)
        elif side == 'smart':
            return re.sub(r'[^\S\n]+$', '', end_result, flags=re.MULTILINE).lstrip('\n')
        else:
            return end_result

    return {'onEndResult': on_end_result}