# Copyright © 2023 the OAI-RNIS Authors

# Licensed under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License. 
# Contact: netsoft@eurecom.fr


from re import M
import connexion
import six
from flask import current_app
from oai_rnis.models.associate_id import AssociateId
from oai_rnis.models.cell_id import CellId
from oai_rnis.models.ecgi import Ecgi
from oai_rnis.models.inline_subscription import InlineSubscription  # noqa: E501
from oai_rnis.models.l2_meas import L2Meas
from oai_rnis.models.l2_meas_cell_info import L2MeasCellInfo
from oai_rnis.models.l2_meas_cell_ue_info import L2MeasCellUEInfo
from oai_rnis.models.link_type import LinkType  # noqa: E501
from oai_rnis.models.ng_bearer_info import NGBearerInfo  # noqa: E501
from oai_rnis.models.plmn_info import PlmnInfo  # noqa: E501
from oai_rnis.models.problem_details import ProblemDetails
from oai_rnis.models.rab_est_notification_erab_qos_parameters import RabEstNotificationErabQosParameters
from oai_rnis.models.rab_est_notification_erab_qos_parameters_qos_information import RabEstNotificationErabQosParametersQosInformation  # noqa: E501
from oai_rnis.models.rab_info import RabInfo
from oai_rnis.models.rab_info_cell_user_info import RabInfoCellUserInfo
from oai_rnis.models.rab_info_erab_info import RabInfoErabInfo
from oai_rnis.models.rab_info_ue_info import RabInfoUeInfo  # noqa: E501
from oai_rnis.models.subscription_link_list import SubscriptionLinkList  # noqa: E501
import oai_rnis.utils.util as util
from oai_rnis.utils.util import configuration
from oai_rnis.models.subscription_link_list_links import SubscriptionLinkListLinks
from oai_rnis.models.subscription_link_list_links_subscription import SubscriptionLinkListLinksSubscription
from oai_rnis.models.time_stamp import TimeStamp
from oai_rnis.models.plmn import Plmn

def layer2_meas_info_get(app_ins_id=None, cell_id=None, ue_ipv4_address=None, ue_ipv6_address=None, nated_ip_address=None, gtp_teid=None, dl_gbr_prb_usage_cell=None, ul_gbr_prb_usage_cell=None, dl_nongbr_prb_usage_cell=None, ul_nongbr_prb_usage_cell=None, dl_total_prb_usage_cell=None, ul_total_prb_usage_cell=None, received_dedicated_preambles_cell=None, received_randomly_selected_preambles_low_range_cell=None, received_randomly_selected_preambles_high_range_cell=None, number_of_active_ue_dl_gbr_cell=None, number_of_active_ue_ul_gbr_cell=None, number_of_active_ue_dl_nongbr_cell=None, number_of_active_ue_ul_nongbr_cell=None, dl_gbr_pdr_cell=None, ul_gbr_pdr_cell=None, dl_nongbr_pdr_cell=None, ul_nongbr_pdr_cell=None, dl_gbr_delay_ue=None, ul_gbr_delay_ue=None, dl_nongbr_delay_ue=None, ul_nongbr_delay_ue=None, dl_gbr_pdr_ue=None, ul_gbr_pdr_ue=None, dl_nongbr_pdr_ue=None, ul_nongbr_pdr_ue=None, dl_gbr_throughput_ue=None, ul_gbr_throughput_ue=None, dl_nongbr_throughput_ue=None, ul_nongbr_throughput_ue=None, dl_gbr_data_volume_ue=None, ul_gbr_data_volume_ue=None, dl_nongbr_data_volume_ue=None, ul_nongbr_data_volume_ue=None):  # noqa: E501
    """Retrieve information on layer 2 measurements

    Queries information about the layer 2 measurements. # noqa: E501

    :param app_ins_id: Application instance identifier
    :type app_ins_id: str
    :param cell_id: Comma separated list of E-UTRAN Cell Identities
    :type cell_id: List[str]
    :param ue_ipv4_address: Comma separated list of IE IPv4 addresses as defined for the type for AssociateId
    :type ue_ipv4_address: List[str]
    :param ue_ipv6_address: Comma separated list of IE IPv6 addresses as defined for the type for AssociateId
    :type ue_ipv6_address: List[str]
    :param nated_ip_address: Comma separated list of IE NATed IP addresses as defined for the type for AssociateId
    :type nated_ip_address: List[str]
    :param gtp_teid: Comma separated list of GTP TEID addresses as defined for the type for AssociateId
    :type gtp_teid: List[str]
    :param dl_gbr_prb_usage_cell: PRB usage for downlink GBR traffic in percentage as defined in ETSI TS 136 314
    :type dl_gbr_prb_usage_cell: int
    :param ul_gbr_prb_usage_cell: PRB usage for uplink GBR traffic in percentage as defined in ETSI TS 136 314
    :type ul_gbr_prb_usage_cell: int
    :param dl_nongbr_prb_usage_cell: PRB usage for downlink non-GBR traffic in percentage as defined in ETSI TS 136 314
    :type dl_nongbr_prb_usage_cell: int
    :param ul_nongbr_prb_usage_cell: PRB usage for uplink non-GBR traffic in percentage as defined in ETSI TS 136 314
    :type ul_nongbr_prb_usage_cell: int
    :param dl_total_prb_usage_cell: PRB usage for total downlink traffic in percentage as defined in ETSI TS 136 314
    :type dl_total_prb_usage_cell: int
    :param ul_total_prb_usage_cell: PRB usage for total uplink traffic in percentage as defined in ETSI TS 136 314
    :type ul_total_prb_usage_cell: int
    :param received_dedicated_preambles_cell: Received dedicated preambles in percentage as defined in ETSI TS 136 314
    :type received_dedicated_preambles_cell: int
    :param received_randomly_selected_preambles_low_range_cell: Received randomly selected preambles in the low range in percentage as defined in ETSI TS 136 314
    :type received_randomly_selected_preambles_low_range_cell: int
    :param received_randomly_selected_preambles_high_range_cell: Received rendomly selected preambles in the high range in percentage as defined in ETSI TS 136 314
    :type received_randomly_selected_preambles_high_range_cell: int
    :param number_of_active_ue_dl_gbr_cell: Number of active UEs with downlink GBR traffic as defined in ETSI TS 136 314
    :type number_of_active_ue_dl_gbr_cell: int
    :param number_of_active_ue_ul_gbr_cell: Number of active UEs with uplink GBR traffic as defined in ETSI TS 136 314
    :type number_of_active_ue_ul_gbr_cell: int
    :param number_of_active_ue_dl_nongbr_cell: Number of active UEs with downlink non-GBR traffic as defined in ETSI TS 136 314
    :type number_of_active_ue_dl_nongbr_cell: int
    :param number_of_active_ue_ul_nongbr_cell: Number of active UEs with uplink non-GBR traffic as defined in ETSI TS 136 314
    :type number_of_active_ue_ul_nongbr_cell: int
    :param dl_gbr_pdr_cell: Packet discard rate for downlink GBR traffic in percentage as defined in ETSI TS 136 314
    :type dl_gbr_pdr_cell: int
    :param ul_gbr_pdr_cell: Packet discard rate for uplink GBR traffic in percentage as defined in ETSI TS 136 314
    :type ul_gbr_pdr_cell: int
    :param dl_nongbr_pdr_cell: Packet discard rate for downlink non-GBR traffic in percentage as defined in ETSI TS 136 314
    :type dl_nongbr_pdr_cell: int
    :param ul_nongbr_pdr_cell: Packet discard rate for uplink non-GBR traffic in percentage as defined in ETSI TS 136 314
    :type ul_nongbr_pdr_cell: int
    :param dl_gbr_delay_ue: Packet delay of downlink GBR traffic of a UE as defined in ETSI TS 136 314
    :type dl_gbr_delay_ue: int
    :param ul_gbr_delay_ue: Packet delay of uplink GBR traffic of a UE as defined in ETSI TS 136 314
    :type ul_gbr_delay_ue: int
    :param dl_nongbr_delay_ue: Packet delay of downlink non-GBR traffic of a UE as defined in ETSI TS 136 314
    :type dl_nongbr_delay_ue: int
    :param ul_nongbr_delay_ue: Packet delay of uplink non-GBR traffic of a UE as defined in ETSI TS 136 314
    :type ul_nongbr_delay_ue: int
    :param dl_gbr_pdr_ue: Packet discard rate of downlink GBR traffic of a UE in percentage as defined in ETSI TS 136 314
    :type dl_gbr_pdr_ue: int
    :param ul_gbr_pdr_ue: Packet discard rate of uplink GBR traffic of a UE in percentage as defined in ETSI TS 136 314
    :type ul_gbr_pdr_ue: int
    :param dl_nongbr_pdr_ue: Packet discard rate of downlink non-GBR traffic of a UE in percentage as defined in ETSI TS 136 314
    :type dl_nongbr_pdr_ue: int
    :param ul_nongbr_pdr_ue: Packet discard rate of uplink non-GBR traffic of a UE in percentage as defined in ETSI TS 136 314
    :type ul_nongbr_pdr_ue: int
    :param dl_gbr_throughput_ue: Scheduled throughput of downlink GBR traffic of a UE as defined in ETSI TS 136 314
    :type dl_gbr_throughput_ue: int
    :param ul_gbr_throughput_ue: Scheduled throughput of uplink GBR traffic of a UE as defined in ETSI TS 136 314
    :type ul_gbr_throughput_ue: int
    :param dl_nongbr_throughput_ue: Scheduled throughput of downlink non-GBR traffic of a UE as defined in ETSI TS 136 314
    :type dl_nongbr_throughput_ue: int
    :param ul_nongbr_throughput_ue: Scheduled throughput of uplink non-GBR traffic of a UE as defined in ETSI TS 136 314
    :type ul_nongbr_throughput_ue: int
    :param dl_gbr_data_volume_ue: Data volume of downlink GBR traffic of a UE as defined in ETSI TS 136 314
    :type dl_gbr_data_volume_ue: int
    :param ul_gbr_data_volume_ue: Data volume of uplink GBR traffic of a UE as defined in ETSI TS 136 314
    :type ul_gbr_data_volume_ue: int
    :param dl_nongbr_data_volume_ue: Data volume of downlink non-GBR traffic of a UE as defined in ETSI TS 136 314
    :type dl_nongbr_data_volume_ue: int
    :param ul_nongbr_data_volume_ue: Data volume of uplink non-GBR traffic of a UE as defined in ETSI TS 136 314
    :type ul_nongbr_data_volume_ue: int

    :rtype: L2Meas
    """
    repository = current_app.config["data_repository"]

    cells_info = []
    cell_ues_info = []
    cells = repository.cell_users
    for cell in cells:
        for user_id in cells[cell]:
            supi = repository.ngap2supi(user_id,cell)
            plmn = None
            #if repository.get_ue_sessions(supi) is not None:
                #plmn = repository.get_ue_sessions(supi)[1].plmn
                #plmn = Plmn(
                #    mcc = plmn.mcc,
                #    mnc = plmn.mnc
                #)
            cell_ues_info.append(L2MeasCellUEInfo(
                associate_id=AssociateId(
                    type=1,
                    value=repository.supi2ips(supi)
                ),
                dl_gbr_data_volume_ue=0,
                dl_gbr_delay_ue=0,
                dl_gbr_pdr_ue=0,
                dl_gbr_throughput_ue=0,
                dl_nongbr_data_volume_ue=0,
                dl_nongbr_delay_ue=0,
                dl_nongbr_throughput_ue=0,
                ecgi=Ecgi(
                    cell_id=cell,
                    plmn= plmn
                ),
                ul_gbr_data_volume_ue=0,
                ul_gbr_delay_ue=0,
                ul_gbr_pdr_ue=0,
                ul_gbr_throughput_ue=0,
                ul_nongbr_data_volume_ue=0,
                ul_nongbr_delay_ue=0,
                ul_nongbr_pdr_ue=0,
                ul_nongbr_throughput_ue=0,
                #kpis = repository.ue_kpis(supi)
            ))

            cells_info.append(L2MeasCellInfo(
            dl_gbr_pdr_cell=0,
            dl_gbr_prb_usage_cell=0,
            dl_nongbr_pdr_cell=0,
            dl_nongbr_prb_usage_cell=0,
            dl_total_prb_usage_cell=0,
            ecgi=Ecgi(
                cell_id= cell,
                plmn= plmn
            ),
            number_of_active_ue_dl_gbr_cell=0,
            number_of_active_ue_dl_nongbr_cell=0,
            number_of_active_ue_ul_gbr_cell=0,
            number_of_active_ue_ul_nongbr_cell=0,
            received_dedicated_preambles_cell=0,
            received_randomly_selected_preambles_high_range_cell=0,
            received_randomly_selected_preambles_low_range_cell=0,
            ul_gbr_pdr_cell=0,
            ul_gbr_prb_usage_cell=0,
            ul_nongbr_pdr_cell=0,
            ul_nongbr_prb_usage_cell=0,
            ul_total_prb_usage_cell=0,
        ))

    #return L2Meas(cells_info, cell_ues_info)

    #return an array of json objects mapping user and their kpis
    #TODO return a standard response
    response = []
    for supi in repository.users:
        print(supi)
        repository.supi2ips(supi)
        response.append({"ueIPs": repository.supi2ips(supi), "KPIs":repository.ue_kpis(supi)})
    return response 


## Todo not available
def ng_bearer_info_get(temp_ue_id=None, ue_ipv4_address=None, ue_ipv6_address=None, nated_ip_address=None, gtp_teid=None, cell_id=None, erab_id=None):  # noqa: E501
    """Retrieve NG-U bearer information related to specific UE(s)

    Queries information about the NG bearer(s) # noqa: E501

    :param temp_ue_id: Comma separated list of temporary identifiers allocated for the specific UE as defined in   ETSI TS 136 413
    :type temp_ue_id: List[str]
    :param ue_ipv4_address: Comma separated list of IE IPv4 addresses as defined for the type for AssociateId
    :type ue_ipv4_address: List[str]
    :param ue_ipv6_address: Comma separated list of IE IPv6 addresses as defined for the type for AssociateId
    :type ue_ipv6_address: List[str]
    :param nated_ip_address: Comma separated list of IE NATed IP addresses as defined for the type for AssociateId
    :type nated_ip_address: List[str]
    :param gtp_teid: Comma separated list of GTP TEID addresses as defined for the type for AssociateId
    :type gtp_teid: List[str]
    :param cell_id: Comma separated list of E-UTRAN Cell Identities
    :type cell_id: List[str]
    :param erab_id: Comma separated list of E-RAB identifiers
    :type erab_id: List[int]

    :rtype: NGBearerInfo
    """
    return 'Not available', 200


def plmn_info_get(app_ins_id):  # noqa: E501
    """Retrieve information on the underlying Mobile Network that the MEC application is associated to

    Queries information about the Mobile Network # noqa: E501

    :param app_ins_id: Comma separated list of Application instance identifiers
    :type app_ins_id: List[str]

    :rtype: List[PlmnInfo]
    """
    repository = current_app.config["data_repository"]
    plmns = []
    for plmn in repository.plmns:
        plmns.append(Plmn(mcc=plmn.mcc, mnc=plmn.mnc))
    PlmnInfo(app_instance_id=app_ins_id,plmn=plmns,time_stamp=TimeStamp())
    return PlmnInfo(app_instance_id=app_ins_id,plmn=plmns,time_stamp=TimeStamp())


def rab_info_get(app_ins_id=None, cell_id=None, ue_ipv4_address=None, ue_ipv6_address=None, nated_ip_address=None, gtp_teid=None, erab_id=None, qci=None, erab_mbr_dl=None, erab_mbr_ul=None, erab_gbr_dl=None, erab_gbr_ul=None):  # noqa: E501
    """Retrieve information on Radio Access Bearers

    Queries information about the Radio Access Bearers # noqa: E501

    :param app_ins_id: Application instance identifier
    :type app_ins_id: str
    :param cell_id: Comma separated list of E-UTRAN Cell Identities
    :type cell_id: List[str]
    :param ue_ipv4_address: Comma separated list of IE IPv4 addresses as defined for the type for AssociateId
    :type ue_ipv4_address: List[str]
    :param ue_ipv6_address: Comma separated list of IE IPv6 addresses as defined for the type for AssociateId
    :type ue_ipv6_address: List[str]
    :param nated_ip_address: Comma separated list of IE NATed IP addresses as defined for the type for AssociateId
    :type nated_ip_address: List[str]
    :param gtp_teid: Comma separated list of GTP TEID addresses as defined for the type for AssociateId
    :type gtp_teid: List[str]
    :param erab_id: E-RAB identifier
    :type erab_id: int
    :param qci: QoS Class Identifier as defined in ETSI TS 123 401
    :type qci: int
    :param erab_mbr_dl: Maximum downlink E-RAB Bit Rate as defined in ETSI TS 123 401
    :type erab_mbr_dl: int
    :param erab_mbr_ul: Maximum uplink E-RAB Bit Rate as defined in ETSI TS 123 401
    :type erab_mbr_ul: int
    :param erab_gbr_dl: Guaranteed downlink E-RAB Bit Rate as defined in ETSI TS 123 401
    :type erab_gbr_dl: int
    :param erab_gbr_ul: Guaranteed uplink E-RAB Bit Rate as defined in ETSI TS 123 401
    :type erab_gbr_ul: int

    :rtype: RabInfo
    """
    #TODO implement filters
    repository = current_app.config["data_repository"]
    cell_users_info = []
    for cell in repository.cell_users:
        for ran_id in repository.cell_users[cell]:
            supi = repository.ngap2supi(ran_id, cell)
            ue_infos = [] 
            _plmn = None
            if supi not in repository.pdu_sessions:
                continue
            for pdus_id in repository.pdu_sessions[supi]:
                session = repository.pdu_sessions[supi][pdus_id]
                if session.qos_flows == None or session.qos_flows == []:
                    continue
                erabs = []
                cnt = 0
                for qos_flow in session.qos_flows:
                    erab = RabInfoErabInfo(
                        erab_id= cnt,
                        erab_qos_parameters= RabEstNotificationErabQosParameters(
                            qci= qos_flow.qfi,
                            qos_information= RabEstNotificationErabQosParametersQosInformation()
                            )
                        )
                    cnt = cnt + 1
                    erabs.append(erab)
                ue_ids = [] 
                ue_ids.append(AssociateId(type=1, value=session.ue_ip))
                if _plmn is None:
                    _plmn = session.plmn
                ue_infos.append(RabInfoUeInfo(associate_id = ue_ids, erab_info = erabs))
            if _plmn == None:
                continue            
            cell_user_info = RabInfoCellUserInfo(
                ecgi= Ecgi(
                    cell_id=cell,
                    plmn= Plmn(
                        mcc= _plmn.mcc,
                        mnc= _plmn.mnc 
                    )
                ),
                ue_info = ue_infos

            )
            cell_users_info.append(cell_user_info)
    return RabInfo(app_instance_id=app_ins_id, cell_user_info=cell_users_info,request_id="0", time_stamp=TimeStamp())


def subscription_link_list_subscriptions_get(subscription_type=None):  # noqa: E501
    """Retrieve information on subscriptions for notifications

    Queries information on subscriptions for notifications # noqa: E501

    :param subscription_type: Filter on a specific subscription type. Permitted values: cell_change, rab_est, rab_mod, rab_rel, meas_rep_ue, nr_meas_rep_ue, timing_advance_ue, ca_reconf, ng_bearer.
    :type subscription_type: str

    :rtype: SubscriptionLinkList
    """
    baselink = f"http://{configuration['application']['host']}:{configuration['application']['port']}/rnis/subscriptions"

    notifservice = current_app.config["notification_service"]
    if subscription_type == '':
        subscription_type = None
    subs = notifservice.get_subscriptions()
    sublist = []
    for type in subs:
        if subscription_type is not None:
            type = subscription_type
        if type == "NewCellSubscription":
            break
        for sub in subs[type]["subscriptions"]:
            sublist.append(
                SubscriptionLinkListLinksSubscription(
                    href=baselink+"/"+sub["id"],
                    subscription_type=sub["subscription"]["subscriptionType"]
                )
            )
        if subscription_type is not None:
            break
    
    return SubscriptionLinkList(
        SubscriptionLinkListLinks(
            _self = LinkType(
                href=baselink
            ),
            subscription=sublist
        )
    )


def subscriptions_delete(subscription_id):  # noqa: E501
    """Cancel an existing subscription

    Cancels an existing subscription, identified by its self-referring URI returned on creation (initial POST) # noqa: E501

    :param subscription_id: Subscription Id, specifically the \&quot;Self-referring URI\&quot; returned in the subscription request
    :type subscription_id: str

    :rtype: None
    """
    if current_app.config["notification_service"].del_subscription(subscription_id):
        return None
    else:
        return None,404


def subscriptions_get(subscription_id):  # noqa: E501
    """Retrieve information on current specific subscription

    Queries information about an existing subscription, identified by its self-referring URI returned on creation (initial POST) # noqa: E501

    :param subscription_id: Subscription Id, specifically the \&quot;Self-referring URI\&quot; returned in the subscription request
    :type subscription_id: str

    :rtype: InlineSubscription
    """
    baselink = ""
    notifservice = current_app.config["notification_service"]
    subs = notifservice.get_subscriptions()
    for type in subs:
        if type != "NewCellSubscriptions":
            for sub in subs[type]["subscriptions"]:
                if sub["id"] == subscription_id :
                    return sub["subscription"]

    return None, 404


def subscriptions_post(body):  # noqa: E501
    """Create a new subscription

    Creates a new subscription to Radio Network Information notifications # noqa: E501

    :param body: Subscription to be created
    :type body: dict | bytes

    :rtype: InlineSubscription
    """
    if connexion.request.is_json:
        body = InlineSubscription.from_dict(connexion.request.get_json())  # noqa: E501
    
    notifserivce = current_app.config["notification_service"]
    return notifserivce.add_subscription(body)


## TODO: Not available
def subscriptions_put(body, subscription_id):  # noqa: E501
    """Modify an existing subscription

    Updates an existing subscription, identified by its self-referring URI returned on creation (initial POST) # noqa: E501

    :param body: Subscription to be modified
    :type body: dict | bytes
    :param subscription_id: Subscription Id, specifically the \&quot;Self-referring URI\&quot; returned in the subscription request
    :type subscription_id: str

    :rtype: InlineSubscription
    """
    if connexion.request.is_json:
        body = InlineSubscription.from_dict(connexion.request.get_json())  # noqa: E501
    return 'Not available',200