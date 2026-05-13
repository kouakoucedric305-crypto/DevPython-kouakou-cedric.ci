#!/usr/bin/env python
"""Django manage.py — Point d'entrée pour les commandes Django."""
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'entreprise_site.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Django non installé.") from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
