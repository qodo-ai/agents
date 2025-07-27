#!/usr/bin/env python3
# /// script
# dependencies = [
#     "ansible"
# ]
# ///

"""
An infrastructure automation example using GPL-licensed dependencies.

This script demonstrates using Ansible for automation tasks.
WARNING: Ansible has a GPL license which may have restrictions.
"""

import subprocess
import tempfile
import os
import yaml
from pathlib import Path


def create_ansible_inventory(hosts: list) -> str:
    """Create a temporary Ansible inventory file."""
    inventory_content = {
        'all': {
            'hosts': {host: {'ansible_host': host} for host in hosts}
        }
    }
    
    # Create temporary inventory file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        yaml.dump(inventory_content, f, default_flow_style=False)
        return f.name


def create_ansible_playbook() -> str:
    """Create a simple Ansible playbook."""
    playbook_content = [
        {
            'name': 'System Information Gathering',
            'hosts': 'all',
            'gather_facts': True,
            'tasks': [
                {
                    'name': 'Get system information',
                    'debug': {
                        'msg': 'System {{ ansible_hostname }} running {{ ansible_os_family }}'
                    }
                },
                {
                    'name': 'Check disk usage',
                    'command': 'df -h',
                    'register': 'disk_usage'
                },
                {
                    'name': 'Display disk usage',
                    'debug': {
                        'var': 'disk_usage.stdout_lines'
                    }
                }
            ]
        }
    ]
    
    # Create temporary playbook file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        yaml.dump(playbook_content, f, default_flow_style=False)
        return f.name


def run_ansible_playbook(inventory_file: str, playbook_file: str, dry_run: bool = True):
    """Run an Ansible playbook."""
    
    cmd = ['ansible-playbook', '-i', inventory_file, playbook_file]
    
    if dry_run:
        cmd.append('--check')
        print("Running in dry-run mode (--check)")
    
    try:
        print(f"Executing: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
            
    except subprocess.CalledProcessError as e:
        print(f"Ansible playbook failed with return code {e.returncode}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        raise
    except FileNotFoundError:
        print("Error: ansible-playbook command not found. Please install Ansible.")
        print("Note: This example demonstrates GPL dependency usage for automation.")
        raise


def main():
    """Main function to demonstrate Ansible automation."""
    
    # Define target hosts (using localhost for demo)
    hosts = ['localhost']
    
    print("Creating Ansible automation example...")
    print("Note: This uses Ansible which has a GPL license")
    
    try:
        # Create temporary files
        inventory_file = create_ansible_inventory(hosts)
        playbook_file = create_ansible_playbook()
        
        print(f"Created inventory: {inventory_file}")
        print(f"Created playbook: {playbook_file}")
        
        # Run the playbook in check mode
        run_ansible_playbook(inventory_file, playbook_file, dry_run=True)
        
    except Exception as e:
        print(f"Error running automation: {e}")
    finally:
        # Cleanup temporary files
        for file_path in [inventory_file, playbook_file]:
            try:
                if file_path and os.path.exists(file_path):
                    os.unlink(file_path)
            except Exception:
                pass


if __name__ == "__main__":
    main()