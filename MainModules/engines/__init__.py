from .bing import Bing
from .duckduckgo import Duckduckgo
from .google import Google
from .yahoo import Yahoo


search_engines_dict = { 
    'google': Google, 
    'bing': Bing, 
    'yahoo': Yahoo,  
    'duckduckgo': Duckduckgo
}
