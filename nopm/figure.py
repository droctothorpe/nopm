import logging
import warnings
from xml.dom import minidom
from xml.parsers.expat import ExpatError

from nopm.models.base import ModelProvider

logger = logging.getLogger(__name__)

PROMPT = """
You an expert XML and SVG developer. You need to generate the XML-representation of a SVG file based on the following description:

{description}

No other languages or tools should be used. Only the raw XML output. This should able to be parsed by SVG renderings conforming to all XML and SVG conventions and specifications. Return ONLY xml output with no markdown or other formatting.
"""


def _is_svg(content: str) -> bool:
    try:
        dom = minidom.parseString(content)
    except ExpatError:
        return False

    if dom.version != "1.0":
        warnings.warn(f"SVG version {dom.version} is not 1.0")
    if dom.encoding != "UTF-8":
        warnings.warn(f"SVG encoding {dom.encoding} is not UTF-8")

    svg = dom.getElementsByTagName("svg")
    if len(svg) != 1: 
        return False
    svg = svg[0]
    if svg.getAttribute("xmlns") != "http://www.w3.org/2000/svg":
        return False
    
    return True

def _try_repair_svg(content: str) -> str:
    content = content.strip()
    content = (
        content.removeprefix("```\n")
        .removeprefix("```xml\n")
        .removeprefix("```svg\n")
        .removesuffix("```")
    )

    if _is_svg(content):
        logger.debug("Repair successful.")
    else:
        logger.error("Unable to repair generated as SVG: %s" % content)
        raise ValueError("Generated content is not SVG and repairs failed.")

    return content

class Figure:
    def __init__(self, model_provider: ModelProvider):
        self.model_provider = model_provider
    
    def generate(self, description: str, file_name: str):
        prompt = PROMPT.format(description=description)
        content = self.model_provider.generate(prompt)

        # Check svg
        if not _is_svg(content):
            content = _try_repair_svg(content)
        
        with open(file_name, "w") as f:
            f.write(content)