from ohmgroups.ohm_groups.utils.stock.quality_inspection import quality_inspection
from ohmgroups.ohm_groups.utils.stock.quality_inspection_reading import property_setter

def after_install():
    quality_inspection()
    property_setter()
