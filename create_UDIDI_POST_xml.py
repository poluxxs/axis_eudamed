import xml.etree.ElementTree as ET
import uuid
from datetime import datetime, timezone


def create_UDIDI_POST_xml(
    devices_xml_list,
    #service_token,
    sender_actor_code,
    #sender_party_id
):
    """
    devices_xml_list: list of XML Elements (Device payloads)
    service_token: EUDAMED token
    sender_actor_code: SRN Actor Code
    sender_party_id: Party ID
    """

    # Generate IDs automatically
    conversation_id = str(uuid.uuid4())
    correlation_id = str(uuid.uuid4())
    message_id = str(uuid.uuid4())

    S = "https://ec.europa.eu/tools/eudamed/dtx/servicemodel/Service/v1"
    M = "https://ec.europa.eu/tools/eudamed/dtx/servicemodel/Message/v1"
    UDIDIData = "https://ec.europa.eu/tools/eudamed/dtx/datamodel/Entity/Device/v1"

    creation_time = datetime.now(timezone.utc)\
        .isoformat()\
        .replace("+00:00", "Z")
    ET.register_namespace("m", M)
    ET.register_namespace("s", S)
    ET.register_namespace("e", "https://ec.europa.eu/tools/eudamed/dtx/datamodel/Entity/v1")
    ET.register_namespace("links", "https://ec.europa.eu/tools/eudamed/dtx/datamodel/Entity/Links/v1")
    ET.register_namespace("commondevice", "https://ec.europa.eu/tools/eudamed/dtx/datamodel/Entity/Device/CommonDevice/v1")
    ET.register_namespace("udidi", "https://ec.europa.eu/tools/eudamed/dtx/datamodel/Entity/UDIDI/v1")
    ET.register_namespace("udidiDatas", UDIDIData)
    ET.register_namespace("lsn", "https://ec.europa.eu/tools/eudamed/dtx/datamodel/Entity/Common/LanguageSpecific/v1")
    ET.register_namespace("marketinfo", "https://ec.europa.eu/tools/eudamed/dtx/datamodel/Entity/MktInfo/MarketInfo/v1")
    ET.register_namespace("commondi", "https://ec.europa.eu/tools/eudamed/dtx/datamodel/Entity/Device/CommonDevice/v1")
    ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")
        
    root = ET.Element(
        "{https://ec.europa.eu/tools/eudamed/dtx/servicemodel/Message/v1}Push",
        {
            "version": "3.0.32",
            "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation":
                "https://ec.europa.eu/tools/eudamed/dtx/servicemodel/Message/v1 "
                "https://webgate.ec.europa.eu/tools/eudamed/dtx/service/Message.xsd"
        }
    )

    # Header fields
    ET.SubElement(root, f"{{{M}}}conversationID").text = conversation_id
    ET.SubElement(root, f"{{{M}}}correlationID").text = correlation_id
    ET.SubElement(root, f"{{{M}}}creationDateTime").text = creation_time
    ET.SubElement(root, f"{{{M}}}messageID").text = message_id

    # Recipient
    recipient = ET.SubElement(root, f"{{{M}}}recipient")

    node = ET.SubElement(recipient, f"{{{M}}}node")
    ET.SubElement(node, f"{{{S}}}nodeActorCode").text = "EUDAMED_MDR"
    ET.SubElement(node, f"{{{S}}}nodeID").text = "eDelivery:EUDAMED"

    service = ET.SubElement(recipient, f"{{{M}}}service")
    #ET.SubElement(service, f"{{{S}}}serviceAccessToken").text = service_token
    ET.SubElement(service, f"{{{S}}}serviceID").text = "UDI_DI"
    ET.SubElement(service, f"{{{S}}}serviceOperation").text = "POST"

    # Payload
    payload = ET.SubElement(root, f"{{{M}}}payload")

    # Insert devices
    for device_xml in devices_xml_list:
        payload.append(device_xml)

    # Sender
    sender = ET.SubElement(root, f"{{{M}}}sender")

    sender_node = ET.SubElement(sender, f"{{{M}}}node")
    ET.SubElement(sender_node, f"{{{S}}}nodeActorCode").text = sender_actor_code
    #ET.SubElement(sender_node, f"{{{S}}}nodeID").text = sender_party_id

    sender_service = ET.SubElement(sender, f"{{{M}}}service")
    ET.SubElement(sender_service, f"{{{S}}}serviceID").text = "REPLY_SERVICE"
    ET.SubElement(sender_service, f"{{{S}}}serviceOperation").text = "GET"

    return root