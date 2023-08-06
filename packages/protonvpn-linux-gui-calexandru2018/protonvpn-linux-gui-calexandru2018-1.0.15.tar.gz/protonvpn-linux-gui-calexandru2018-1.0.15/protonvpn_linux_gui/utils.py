
from protonvpn_cli_ng.protonvpn_cli.utils import (
    pull_server_data,
    get_servers,
    get_country_name,
    get_server_value,
    get_config_value,
    set_config_value,
    check_root,
    is_connected,
    get_ip_info
)

def prepare_initilizer(username_field, password_field, interface):
    """Collects and prepares user input from login window.
    Returns:
    ----
    - A dictionary with username, password, plan type and default protocol.
    """
    # Get user specified protocol
    protonvpn_plan = ''
    openvpn_protocol = 'tcp' if interface.get_object('protocol_tcp_checkbox').get_active() else 'udp'
    
    if len(username_field) == 0 or len(password_field) == 0:
        return

    protonvpn_plans = {
        '1': interface.get_object('member_free').get_active(),
        '2': interface.get_object('member_basic').get_active(),
        '3': interface.get_object('member_plus').get_active(),
        '4': interface.get_object('member_visionary').get_active()
    }

    # Get user plan
    for k,v in protonvpn_plans.items():
        if v == True:
            protonvpn_plan = k
            break
    
    user_data = {
        'username': username_field,
        'password': password_field,
        'protonvpn_plan': int(protonvpn_plan),
        'openvpn_protocol': openvpn_protocol
    }

    return user_data

def load_on_start(interface):
    """Loads main window on start
    """
    server_list_object = interface.get_object("ServerListStore")
    killswitch_toggle = interface.get_object("killswitch_toggle_button")

    update_labels_status(interface)

    # Set killswitch button to ON or OFF, depending on status
    killswitch_enabled = get_config_value("USER", "killswitch")
    if int(killswitch_enabled) == 1:
        killswitch_toggle.set_active(True)

    # Populate server list
    populate_server_list(server_list_object)

def update_labels_status(interface):
    """Updates label statuses
    """
    vpn_status_label = interface.get_object("vpn_status_label")
    dns_status_label = interface.get_object("dns_status_label")
    ip_label = interface.get_object("ip_label")
    country_label = interface.get_object("country_label")


    # Check VPN status
    if is_connected() != True:
        vpn_status_label.set_markup('<span>Not Running</span>')
    else:
        vpn_status_label.set_markup('<span foreground="#4E9A06">Running</span>')
    
    # Check DNS status
    dns_enabled = get_config_value("USER", "dns_leak_protection")
    if int(dns_enabled) != 1:
        dns_status_label.set_markup('<span>Not Enabled</span>')
    else:
        dns_status_label.set_markup('<span foreground="#4E9A06">Enabled</span>')

    ip, isp, country = get_ip_info(gui_enbled=True)
    
    ip = "<span>" + ip + "</span>"
    country_isp = "<span>" + country + "/" + isp + "</span>"

    ip_label.set_markup(ip)
    country_label.set_markup(country_isp)

def load_configurations(interface):
    pref_dialog = interface.get_object("ConfigurationsWindow")
    
    # Load user configurations before showing the window
    username = get_config_value("USER", "username")
    dns_leak_protection = get_config_value("USER", "dns_leak_protection")
    custom_dns = get_config_value("USER", "custom_dns")
    tier = int(get_config_value("USER", "tier")) + 1
    default_protocol = get_config_value("USER", "default_protocol")

    # Populate username
    username_field = interface.get_object("update_username_input")
    username_field.set_text(username)

    # To-do DNS combobox
    dns_combobox = interface.get_object("dns_preferens_combobox")
    dns_custom_input = interface.get_object("dns_custom_input")

    # DNS ComboBox
    # 0 - Leak Protection Enabled
    # 1 - Custom DNS
    # 2 - None

    if dns_leak_protection == '1':
        dns_combobox.set_active(0)
    elif dns_leak_protection != '1' and custom_dns.lower != "none":
        dns_combobox.set_active(1)
        dns_custom_input.set_property('sensitive', True)
    else:
        dns_combobox.set_active(2)

    dns_custom_input.set_text(custom_dns)

    # Populate ProtonVPN Plan
    protonvpn_plans = {
        1: interface.get_object("member_free_update_checkbox"),
        2: interface.get_object("member_basic_update_checkbox"),
        3: interface.get_object("member_plus_update_checkbox"),
        4: interface.get_object("member_visionary_update_checkbox")
    }

    for tier_val, object in protonvpn_plans.items():
        if tier_val == tier:
            object.set_active(True)
            break

    # Populate OpenVPN Protocol        
    interface.get_object("protocol_tcp_update_checkbox").set_active(True) if default_protocol == "tcp" else interface.get_object("protocol_udp_update_checkbox").set_active(True)
    pref_dialog.show()

    # To-do Split Tunelling

    # To-do Purge Configurations

def populate_server_list(server_list_object):
    """Populates the list with all servers.
    """
    pull_server_data(force=True)

    features = {0: "Normal", 1: "Secure-Core", 2: "Tor", 4: "P2P"}
    server_tiers = {0: "F", 1: "B", 2: "P"}

    servers = get_servers()

    # Country with respective servers, ex: PT#02
    countries = {}
    for server in servers:
        country = get_country_name(server["ExitCountry"])
        if country not in countries.keys():
            countries[country] = []
        countries[country].append(server["Name"])

    country_servers = {}            
    for country in countries:
        country_servers[country] = sorted(
            countries[country],
            key=lambda s: get_server_value(s, "Load", servers)
        )
    server_list_object.clear()
    for country in country_servers:
        for servername in country_servers[country]:
            load = str(get_server_value(servername, "Load", servers)).rjust(3, " ")
            load = load + "%"

            feature = features[get_server_value(servername, 'Features', servers)]

            tier = server_tiers[get_server_value(servername, "Tier", servers)]

            server_list_object.append([country, servername, tier, load, feature])