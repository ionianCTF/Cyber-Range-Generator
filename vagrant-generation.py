import os
import subprocess
import json
from datetime import datetime

def run_nmap_scan(target):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_xml = f"scan_results_{timestamp}.xml"
    output_json = f"scan_results_{timestamp}.json"
    
    # Run the nmap scan
    nmap_command = [
        "sudo", "nmap", "-sS", "-sU", "-p-", "-A", "-sV", 
        "--script", "smb-enum-users,snmp-brute,ftp-anon",
        "-oX", output_xml, target
    ]
    subprocess.run(nmap_command, check=True)
    
    # Convert XML to JSON
    xslt_command = ["xsltproc", output_xml]
    with open(output_json, "w") as json_file:
        subprocess.run(xslt_command, stdout=json_file, check=True)
    
    print(f"Scan complete. Results saved as {output_json}")
    return output_json

def load_json_results(json_file):
    with open(json_file, "r") as f:
        return json.load(f)

def create_vagrantfile(json_data, output_file="Vagrantfile"):
    systems = []
    for host in json_data.get("scan", {}).get("target", []):
        os_name = host.get("os", {}).get("name", "ubuntu")
        ip = host.get("ip", "192.168.33.10")
        ports = host.get("ports", [])
        services = [
            {"port": p.get("port"), "name": p.get("service", {}).get("name"), "version": p.get("service", {}).get("version")}
            for p in ports if p.get("state") == "open"
        ]
        
        vm_name = f"vm_{ip.replace('.', '_')}"
        systems.append({
            "name": vm_name,
            "os": os_name,
            "ip": ip,
            "services": services
        })
    
    # Write Vagrantfile
    with open(output_file, "w") as vagrant_file:
        vagrant_file.write("Vagrant.configure(\"2\") do |config|\n")
        for system in systems:
            vagrant_file.write(f"""
  config.vm.define "{system['name']}" do |{system['name']}|
    {system['name']}.vm.box = "{system['os']}"
    {system['name']}.vm.network "private_network", ip: "{system['ip']}"
    {system['name']}.vm.provision "shell", inline: <<-SHELL
      apt-get update
      apt-get install -y docker.io
""")
            for service in system['services']:
                if service["name"] == "http" and "Apache" in (service.get("version") or ""):
                    vagrant_file.write(f"""
      docker run -d -p {service['port']}:{service['port']} httpd:{service['version'].split()[1]}
""")
            vagrant_file.write("    SHELL\n  end\n")
        vagrant_file.write("end\n")
    print(f"Vagrantfile created: {output_file}")

if __name__ == "__main__":
    target = input("Enter target IP or hostname: ")
    json_file = run_nmap_scan(target)
    json_data = load_json_results(json_file)
    create_vagrantfile(json_data)
