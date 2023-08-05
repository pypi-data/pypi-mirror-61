
import re
import logging

from cloudshell.core.logger.qs_logger import get_qs_logger
from cloudshell.api.cloudshell_api import CloudShellAPISession


def get_logger(context):
    """

    :return: logger according to cloudshell standards.
    """

    logger = get_qs_logger(log_group='traffic_shells', log_file_prefix=context.resource.name)
    logger.setLevel(logging.DEBUG)
    return logger


def get_reservation_ports(session, reservation_id, model_name='Generic Traffic Generator Port'):
    """ Get all Generic Traffic Generator Port in reservation.

    :return: list of all Generic Traffic Generator Port resource objects in reservation
    """

    reservation_ports = []
    reservation = session.GetReservationDetails(reservation_id).ReservationDescription
    for resource in reservation.Resources:
        if resource.ResourceModelName == model_name:
            reservation_ports.append(resource)
    return reservation_ports


def get_reservation_resources(session, reservation_id, *models):
    """ Get all resources of given models in reservation.

    :param session: CloudShell session
    :type session: cloudshell.api.cloudshell_api.CloudShellAPISession
    :param reservation_id: active reservation ID
    :param models: list of requested models
    :return: list of all resources of models in reservation
    """

    models_resources = []
    reservation = session.GetReservationDetails(reservation_id).ReservationDescription
    for resource in reservation.Resources:
        if resource.ResourceModelName in models:
            models_resources.append(resource)
    return models_resources


def get_family_attribute(context, resource, attribute):
    cs_session = CloudShellAPISession(host=context.connectivity.server_address,
                                      token_id=context.connectivity.admin_auth_token,
                                      domain=context.reservation.domain)
    return cs_session.GetAttributeValue(resource.Name, _family_attribute_name(resource, attribute))


def set_family_attribute(context, resource, attribute, value):
    cs_session = CloudShellAPISession(host=context.connectivity.server_address,
                                      token_id=context.connectivity.admin_auth_token,
                                      domain=context.reservation.domain)
    cs_session.SetAttributeValue(resource.Name, _family_attribute_name(resource, attribute), value)


def get_address(port_resource):
    return re.sub('M|PG[0-9]+\/|P', '', port_resource.FullAddress)


def is_blocking(blocking):
    return True if blocking.lower() == "true" else False


def _family_attribute_name(resource, attribute):
    family_attribute_name = attribute
    if resource.ResourceFamilyName.startswith('CS_'):
        family_attribute_name = resource.ResourceFamilyName + '.' + family_attribute_name
    return family_attribute_name
