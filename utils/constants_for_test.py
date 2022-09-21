# raw domain for check
raw_domain_check_data = [
    ("", None),
    ("ksjdhfskj", None),
    ("example.com", "example.com"),
    ("http://example.com", "example.com"),
    ("https://www.example.com", "example.com"),
    ("'https://www.e{xam}ple.com'", "example.com"),
    ("https://edward.example.com", "example.com"),
    ("https://example.com.hk", "example.com.hk"),
    ("ftp://example.com", None),
]

# correct results
correct_string_results = [
    ("freedom.net.tw", "a", "122.146.12.7"),
    ("example.com", "aaaa", "2606:2800:220:1:248:1893:25c8:1946"),
    ("freedom.net.tw", "mx", "0 freedom-net-tw.mail.protection.outlook.com."),
    ("example.com", "www", "www.example.com")
]

correct_list_results = [
    ("freedom.net.tw", "ns", {'dns1.freedom.net.tw', 'dns2.freedom.net.tw', 'dns3.freedom.net.tw'}),
    ("freedom.net.tw", "txt", {'"amazonses:fq9kplq+n2QZma81nrX1HqwzW1clBmAjop8dUW0TUAE="',
                               '"facebook-domain-verification=kif9w8a0h43nkf04g2jpuoh0shfli3"',
                               '"64290fcgkikb97qpqusspc21la"',
                               '"TOTFDF29VVG84SWGKEA9DNFZ9GVNLSKX1IFTRSDY"',
                               '"1password-site-verification=L472XE5IXJFWXE6P6NNVS7ADSY"',
                               '"v=spf1 mx ip4:122.146.12.9 ip4:122.146.12.10 ip4:122.146.12.30 ip4:208.64.224.60 include:spf.protection.outlook.com include:amazonses.com include:mailgun.org ~all"',
                               '"google-site-verification=P1h5z2UCOpDPBweJ8G9d5VCpLdQ0E27b8yl11N8NFPY"'}
     ),
    ("freedom.net.tw", "ipv4", {'104.236.202.184', '128.199.119.242', '122.146.12.30'}),
    ("example.com", "ipv6", {'2001:500:8f::53', '2001:500:8d::53'})
]

# a
different_incorrect_a_record = (
    "12398320548",  # wrong ip
    "123.123.123",  # wrong ip
    "123sdf.423.853r",  # wrong ip
    "256.256.0.1",  # wrong ip
    "127.0.0.1",  # local host
    "255.255.255.255",  # special domain
    "0.0.0.0",  # special domain
    "0.42.42.42",  # can't start with 0, used for current software network
    "10.234.345.7",  # Used for local communications within a private network.
    "192.168.55.12",  # Used for local communications within a private network
    "172.16.4.567",  # Used for local communications within a private network.
    "233.252.0.0",  # Assigned as MCAST-TEST-NET, documentation and examples.
    "224.0.0.1",  # In use for IP multicast.[10] (Former Class D network.)
    "240.3.157.6",  # reserved for future use
)

# aaaa
different_incorrect_aaaa_record = (
    "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff",  # Default Route
    "::",  # unspecified address
    "100::ffff:ffff:ffff:ffff",  # Discard Prefix
    "2001::ffff:ffff:ffff:ffff:ffff:ffff",  # Teredo tunneling
    "2001:2f:ffff:ffff:ffff:ffff:ffff:ffff",  # ORCHIDv2
    "2001:db8:ffff:ffff:ffff:ffff:ffff:ffff",  # Addresses used in documentation and example source code
    "2002:ffff:ffff:ffff:ffff:ffff:ffff:ffff",  # The 6to4 addressing scheme
    "fdff:ffff:ffff:ffff:ffff:ffff:ffff:ffff",  # Unique Local Address
    "fe80::ffff:ffff:ffff:ffff",  # Link-local Address
    "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff"  # Multicast Address
)
