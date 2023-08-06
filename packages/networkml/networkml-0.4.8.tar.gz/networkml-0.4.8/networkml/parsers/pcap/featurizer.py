from collections import defaultdict

import numpy as np

from networkml.parsers.pcap.pcap_utils import extract_macs
from networkml.parsers.pcap.pcap_utils import get_ip_port
from networkml.parsers.pcap.pcap_utils import get_source
from networkml.parsers.pcap.pcap_utils import is_external
from networkml.parsers.pcap.pcap_utils import is_private
from networkml.parsers.pcap.pcap_utils import is_protocol


def extract_features(session_dict, capture_source=None, max_port=1024):
    '''
    Extracts netflow level features from packet capture.

    Args:
        pcap_path: path to the packet capture to process into features
        max_port:  Maximum port to get features on (default to reading config)

    Returns:
        feature_vector: Vector containing the featurized representation
                        of the input pcap.
    '''

    address_type = 'MAC'

    # If the capture source isn't specified, default to the most used address
    if capture_source is None:
        capture_source = get_source(session_dict, address_type=address_type)
    capture_ip_source = get_source(session_dict, address_type='IP')

    # Initialize some counter variables
    num_sport_init = [0]*max_port
    num_dport_init = [0]*max_port
    num_sport_rec = [0]*max_port
    num_dport_rec = [0]*max_port

    num_sessions_init = 0
    num_external_init = 0
    num_tcp_sess_init = 0
    num_udp_sess_init = 0
    num_icmp_sess_init = 0

    num_sessions_rec = 0
    num_external_rec = 0
    num_tcp_sess_rec = 0
    num_udp_sess_rec = 0
    num_icmp_sess_rec = 0

    # Iterate over all sessions and aggregate the info
    other_ips = defaultdict(int)
    for key, session in session_dict.items():
        address_1, port_1 = get_ip_port(key[0])
        address_2, port_2 = get_ip_port(key[1])

        # Get the first packet and grab the macs from it
        first_packet = session[0][1]
        macs = extract_macs(first_packet)
        if macs is None:
            continue
        source_mac, destination_mac = macs

        # If the source is the cpature source
        if (source_mac == capture_source
                or address_1 == capture_source):

            if is_private(address_2):
                other_ips[address_2] += 1

            num_sessions_init += 1
            num_external_init += is_external(address_1, address_2)
            num_tcp_sess_init += is_protocol(session, '06')
            num_udp_sess_init += is_protocol(session, '11')
            num_icmp_sess_init += is_protocol(session, '01')

            if int(port_1) < max_port:
                num_sport_init[int(port_1)] += 1

            if int(port_2) < max_port:
                num_dport_init[int(port_2)] += 1

        # If the destination is the capture source
        if (destination_mac == capture_source
                or address_2 == capture_source):
            if is_private(address_1):
                other_ips[address_1] += 1

            num_sessions_rec += 1
            num_external_rec += is_external(address_2, address_1)
            num_tcp_sess_rec += is_protocol(session, '06')
            num_udp_sess_rec += is_protocol(session, '11')
            num_icmp_sess_rec += is_protocol(session, '01')

            if int(port_1) < max_port:
                num_sport_rec[int(port_1)] += 1
            if int(port_2) < max_port:
                num_dport_rec[int(port_2)] += 1

    num_port_sess = np.concatenate(
        (
            num_sport_init,
            num_dport_init,
            num_sport_rec,
            num_dport_rec
        ),
        axis=0
    )

    if num_sessions_init == 0:
        num_sessions_init += 1
    if num_sessions_rec == 0:
        num_sessions_rec += 1

    num_port_sess = np.asarray(num_port_sess) / \
        (num_sessions_init+num_sessions_rec)

    extra_features = [0]*8
    extra_features[0] = num_external_init/num_sessions_init
    extra_features[1] = num_tcp_sess_init/num_sessions_init
    extra_features[2] = num_udp_sess_init/num_sessions_init
    extra_features[3] = num_icmp_sess_init/num_sessions_init

    extra_features[4] = num_external_rec/num_sessions_rec
    extra_features[5] = num_tcp_sess_rec/num_sessions_rec
    extra_features[6] = num_udp_sess_rec/num_sessions_rec
    extra_features[7] = num_icmp_sess_rec/num_sessions_rec

    feature_vector = np.concatenate((num_port_sess, extra_features), axis=0)
    return feature_vector, capture_source, list(other_ips.keys()), capture_ip_source
