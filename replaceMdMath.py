import re
import sys

USAGE_MSG = ''

MATH_IMAGE_PATTERN = r'(!\[math_\d\]\(.+\d\.png\))'
UNLABELED_MATH_PATTERN = r'(\$\$[^$]+\$\$)'
LABELED_MATH_PATTERN = r'(math_\d\n\$\$[^$]+\$\$)'
MATH_SECTION_PATTERN = r'### Math Blocks'
