#!/usr/bin/env python3
"""Deterministic proxy to test intended trigger coverage (NOT actual LLM auto invocation)."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
from install_activation import is_purrnet_project
from route_docs import norm, term_found

# Unique identifiers where the skill is a useful reference, even without a known project.
EXPLICIT = ('purrnet','purrdiction','purrlobby','purrvoice','purrtransport','purrchat','purrnet-expert','purrnet/purrnet','dev.purrnet.purrnet','dev.purrnet.purrdiction','predictedidentity','predictedhierarchy','predictedobjectid','predictedmodule','predictedifowned','predictedphysicscallbacks','syncbigdata','synctexturefile','syncvar','synclist','syncdictionary','synclazyref','serverrpc','observersrpc','targetrpc','networktransform','networkrigidbody','networkanimator','networkidentity','networkbehaviour','networkmanager','getclientpayload','predictedtransform','onplayerjoinedscene','onplayerloadedscene','onplayerunloadedscene','getclientplayload')
# Other engines / netcodes without PurrNet should not trigger automatically.
FOREIGN = ('fishnet', 'mirror networking', 'netcode for gameobjects','ngo multiplayer','photon fusion','unreal replication','godot multiplayer','netcode for entities')
NETWORK = ('network','networking','multiplayer','multijoueur','reseau','en ligne','online play','coop','co-op','p2p','serveur','server','dedicated','client','owner','ownership','rpc','replication','replication','synchronis','sync','predic','rollback','latenc','lag','jitter','trembl','saccad','desync','desynchronis','deconnexion','connexion','reconnect','matchmaking','lobby','projectile','inventory','inventaire','late join','spawn','packet loss','paquet perdu','host','joueur','player','tir','bullet','rtt','2 clients','deux clients','deuxieme pc','second pc','client build','healthbar','hp bar','remote player','joueur distant','animation reseau','lag compensation','networktransform','networkanimator','networkrigidbody','networkmanager','networkbehaviour','networkidentity','syncvar','synclist','syncinput','serverrpc','observersrpc')
STEMS=('network', 'replic', 'synchron', 'predic', 'latenc', 'trembl', 'saccad', 'desync', 'desynchron', 'reconnect', 'deconnex', 'teleport', 'spawn', 'inventa', 'multijou', 'projectil', 'connect', 'rubber band','dupliqu','doubl','steamworks','onspawned','ontick','bitpacker','serializ','paquet','perdu','erreur','exception','non recu','non reçu','reste vide','empty list','scene load')
OFFLINE = ('shader','ui locale','offline ui','cinematique','cutscene','postprocessing','post-processing','material shader','single player save','sauvegarde solo','single-player','single player','offline hud','local single-player','menu purement local','inspector custom','editor window')

def detect(task: str, project_is_purrnet: bool=False) -> dict:
    t=norm(task)
    explicit=[s for s in EXPLICIT if term_found(t,s)]
    foreign=[s for s in FOREIGN if term_found(t,s)]
    network=[s for s in NETWORK if term_found(t,s)]
    network += [s+'*' for s in STEMS if re.search(r'(?<!\w)'+re.escape(norm(s))+r'\w*',t)]
    # Contextual high-signal debugging: avoid treating every ordinary Unity build
    # or invisible GameObject as a network issue when the project is unknown.
    if project_is_purrnet and (re.search(r'\bil2cpp\b.*\b(crash|panne|error|erreur|echou|failed|build)\b',t)
              or re.search(r'\b(gameobject|objet)\b.*\b(invisible|pas visible|not visible)\b.*\b(scene|chargement)\b',t)):
        network.append('purrnet-specific runtime context')
    offline=[s for s in OFFLINE if term_found(t,s)]
    # Generic class names can occur in Mirror/FishNet questions. Do not steal an explicit
    # foreign-netcode request unless the user names PurrNet / an intended migration.
    strong_explicit=any(x in explicit for x in ('purrnet','purrdiction','purrlobby','purrvoice','purrtransport','purrnet-expert','dev.purrnet.purrnet','dev.purrnet.purrdiction'))
    if explicit and (not foreign or project_is_purrnet or strong_explicit) and not re.search(r'\b(?:no|not|without|sans|pas(?:\s+de)?|not using)\s+purrnet\b', t):active=True; reason='explicit PurrNet ecosystem mention'
    elif foreign and not project_is_purrnet:active=False;reason='different networking stack, no PurrNet project'
    elif project_is_purrnet and network:active=True;reason='implicit multiplayer symptom in known PurrNet Unity project'
    else:active=False;reason='no PurrNet evidence or network scope'
    if offline and not explicit and all(x in ('player','joueur') for x in network):active=False;reason='offline-only task'
    return {'should_suggest_skill':active,'reason':reason,'project_is_purrnet':project_is_purrnet,'explicit':explicit,'network_matches':network[:12],'foreign':foreign,
            'caveat':'Heuristic diagnostic, not a measurement of an agent model automatically loading SKILL.md.'}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('task')
    p.add_argument('--project',type=Path)
    p.add_argument('--purrnet-project',action='store_true',help='simulation flag for tests')
    a=p.parse_args(argv)
    enabled=a.purrnet_project or (bool(a.project) and is_purrnet_project(a.project.resolve()))
    print(json.dumps(detect(a.task,enabled),ensure_ascii=False,indent=2))
    return 0
if __name__=='__main__':raise SystemExit(main())
