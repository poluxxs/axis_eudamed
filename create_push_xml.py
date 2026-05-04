import xml.etree.ElementTree as ET
import uuid
from datetime import datetime, timezone


def create_push_xml(
    devices_xml_list,
    service_token,
    sender_actor_code,
    sender_party_id
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

    creation_time = datetime.now(timezone.utc)\
        .isoformat()\
        .replace("+00:00", "Z")

    # Root
    root = ET.Element(
        "m:Push",
        {
            "version": "3.0.30",
            "xmlns:s": "https://ec.europa.eu/tools/eudamed/dtx/servicemodel/Service/v1",
            "xmlns:links": "https://ec.europa.eu/tools/eudamed/dtx/datamodel/Entity/Links/v1",
            "xmlns:basicudi": "https://ec.europa.eu/tools/eudamed/dtx/datamodel/Entity/Device/BasicUDI/v1",
            "xmlns:udidi": "https://ec.europa.eu/tools/eudamed/dtx/datamodel/Entity/UDIDI/v1",
            "xmlns:device": "https://ec.europa.eu/tools/eudamed/dtx/datamodel/Entity/Device/v1",
            "xmlns:lsn": "https://ec.europa.eu/tools/eudamed/dtx/datamodel/Entity/Common/LanguageSpecific/v1",
            "xmlns:marketinfo": "https://ec.europa.eu/tools/eudamed/dtx/datamodel/Entity/MktInfo/MarketInfo/v1",
            "xmlns:commondi": "https://ec.europa.eu/tools/eudamed/dtx/datamodel/Entity/Device/CommonDevice/v1",
            "xmlns:m": "https://ec.europa.eu/tools/eudamed/dtx/servicemodel/Message/v1",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"
        }
    )

    # Header fields
    ET.SubElement(root, "m:conversationID").text = conversation_id
    ET.SubElement(root, "m:correlationID").text = correlation_id
    ET.SubElement(root, "m:creationDateTime").text = creation_time
    ET.SubElement(root, "m:messageID").text = message_id

    # Recipient
    recipient = ET.SubElement(root, "m:recipient")

    node = ET.SubElement(recipient, "m:node")
    ET.SubElement(node, "s:nodeActorCode").text = "EUDAMED"
    ET.SubElement(node, "s:nodeID").text = "eDelivery:EUDAMED"

    service = ET.SubElement(recipient, "m:service")
    ET.SubElement(service, "s:serviceAccessToken").text = service_token
    ET.SubElement(service, "s:serviceID").text = "DEVICE"
    ET.SubElement(service, "s:serviceOperation").text = "POST"

    # Payload
    payload = ET.SubElement(root, "m:payload")

    # Insert devices
    for device_xml in devices_xml_list:
        payload.append(device_xml)

    # Sender
    sender = ET.SubElement(root, "m:sender")

    sender_node = ET.SubElement(sender, "m:node")
    ET.SubElement(sender_node, "s:nodeActorCode").text = sender_actor_code
    ET.SubElement(sender_node, "s:nodeID").text = sender_party_id

    sender_service = ET.SubElement(sender, "m:service")
    ET.SubElement(sender_service, "s:serviceID").text = "DEVICE"
    ET.SubElement(sender_service, "s:serviceOperation").text = "POST"

    return root