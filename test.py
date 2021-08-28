import pihole as ph

pihole = ph.PiHole("192.168.1.25")
pihole.refresh

domains = pihole.getGraphData()["domains"]
values = [*domains.values()]
print(domains)
print(values)
