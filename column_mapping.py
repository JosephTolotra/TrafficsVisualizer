# Créer un dictionnaire de correspondance entre les noms de colonnes et leurs accronyms
column_mapping = {
    'ts': 'TimeStamp Start',
    'te': 'TimeStamp End',
    'td': 'Total Duration',
    'sa': 'Source Address',
    'da': 'Destination Address',
    'sp': 'Source port',
    'dp': 'Destination port',
    'pr': 'Protocole',
    'flg': 'TCP Flags',
    'fwd': 'Forwarding Status',
    'stos': 'Source Type of Service',
    'ipkt': 'Input Packet',
    'ibyt': 'Input Bytes',
    'opkt': 'Output Packet',
    'obyt':'Output Bytes',
    'in': 'Input Interface',
    'out':'Output Interface',
    'sas':'Source AS',
    'das':'Destination AS',
    'smk': 'Source Mask',
    'dmk':'Destination Mask',
    'dtos':'Destination Type of Service',
    'dir': 'Direction - Direction du flux (entrant ou sortant)',
    'nh' : 'Next Hop - Adresse IP du prochain saut',
    'nhb' : 'BGP Next Hop - Adresse IP du prochain saut BGP',
    'svln' : 'Source VLAN - VLAN source',
    'dvln' : 'Destination VLAN - VLAN de destination',
    'ismc' : 'Input Source MAC',
    'odmc' : 'Output Destination MAC',
    'idmc' : 'Input Destination MAC',
    'osmc' : 'Output Source MAC',
    'mpls1 à mpls10' : 'Étiquettes MPLS',
    'cl' : 'Class of Service - Classe de service',
    'sl' : 'Source Location - Emplacement source',
    'al' : "Application Label - Étiquette de l'\ application",
    'ra': 'Router Address - Adresse IP du routeur',
    'eng' : "Engine Type/ID - Type/ID de l'\engine",
    'exid' : "Exporter ID - Identifiant de l'\exportateur",
    'tr' : 'Traffic Index - Indice de trafic',
}
