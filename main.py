from itm_parser.itm_parser import ITMParser, Protocol_State


print("Hello from main")
itm_parser = ITMParser()
itm_parser.parse(0x01)
itm_parser.parse(0x41)
