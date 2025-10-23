#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module des catégories de compétences
Définit toutes les catégories et la logique de catégorisation
"""

from typing import Dict, List

# Définition complète des catégories
# ------------------------------
# CATEGORIES
# ------------------------------
CATEGORIES = {
    'Intelligence Artificielle et ML': [
        'chatgpt', 'gpt', 'gpt-3', 'gpt-4', 'gpt-5', 'claude', 'dall·e', 'dall-e',
        'midjourney', 'stable diffusion', 'stable diffusion xl', 'controlnet',
        'llm', 'llama', 'mistral', 'gemini', 'copilot', 'bard', 'palm',
        'hugging face', 'openai', 'anthropic', 'intelligence artificielle', 'ia', 'ai',
        'machine learning', 'deep learning', 'reinforcement learning',
        'apprentissage automatique', 'neural', 'réseau de neurones',
        'transformer', 'attention', 'bert', 'embeddings', 'vecteur',
        'prompt engineering', 'prompt tuning', 'instruction tuning', 'LoRA',
        'fine-tuning', 'fine tuning', 'finetuning', 'rag', 'retrieval augmented',
        'few-shot', 'zero-shot', 'chain-of-thought', 'langchain', 'llamaindex',
        'semantic search', 'nlp', 'traitement du langage', 'natural language processing',
        'computer vision', 'vision par ordinateur', 'ocr', 'reconnaissance',
        'génération', 'generative', 'génératif', 'synthèse', 'chatbot',
        'tensorflow', 'pytorch', 'keras', 'jax', 'fastai', 'scikit-learn', 'scikit',
        'xgboost', 'lightgbm', 'catboost', 'onnx', 'onnx runtime', 'mlflow', 'wandb',
        'weights & biases', 'mlops', 'ml ops', 'déploiement de modèles', 'serving',
        'inference', 'model training', 'entraînement', 'hyperparameter',
        'hyperparameter tuning', 'optimization', 'gan', 'autoencoder', 'diffusion',
        'attention mechanism', 'self-supervised', 'transfer learning', 'meta-learning',
        'federated learning', 'recommender system', 'anomaly detection',
        'time series forecasting', 'éthique ia', 'biais', 'fairness', 'explicabilité',
        'xai', 'shap', 'gouvernance ia', 'responsible ai', 'ai safety',
        'annotation', 'labeling', 'dataset', 'augmentation', 'preprocessing',
        'feature engineering', 'embedding', 'tokenization', 'vectorisation',
        'gym', 'openai gym', 'trax', 'paddlepaddle', 'detectron2', 'deepmind dm'
    ],
    'Langages de programmation': [
        'python', 'javascript', 'java', 'c++', 'c#', 'ruby', 'php', 'go', 'rust',
        'typescript', 'swift', 'kotlin', 'scala', 'perl', 'bash', 'shell', 'powershell',
        'sql', 'r', 'matlab', 'julia', 'c', 'cobol', 'fortran', 'fortran 77',
        'assembly', 'vba', 'lua', 'dart', 'groovy', 'vb.net', 'objective-c',
        'haskell', 'lisp', 'prolog', 'erlang', 'elixir', 'nim', 'crystal', 'f#', 'elm', 'scala.js', 'vhdl', 'verilog'
    ],
    'Architecture et Conception': [
        'architecture', 'design pattern', 'microservices', 'monolithe',
        'architecture distribuée', 'soa', 'event-driven', 'cqrs', 'event sourcing',
        'architecture hexagonale', 'clean architecture', 'ddd', 'domain driven design',
        'uml', 'merise', 'conception', 'modélisation', 'architecture cloud',
        'serverless', 'architecture n-tiers', 'mvc', 'mvvm', 'solid', 'dry',
        'grasp', 'pattern factory', 'singleton', 'observer', 'strategy',
        'conception logicielle', 'scalabilité', 'performance', 'maintenabilité'
    ],
    'Frameworks et bibliothèques': [
        'react', 'angular', 'vue', 'django', 'flask', 'spring', 'node', 'express',
        'fastapi', 'laravel', 'symfony', '.net', 'jquery', 'bootstrap', 'tailwind',
        'next.js', 'nuxt', 'svelte', 'spring boot', 'hibernate', 'struts', 'asp.net',
        'entity framework', 'wpf', 'winforms', 'electron', 'qt', 'gtk', 'xamarin',
        'blazor', 'nestjs', 'fastify', 'lit', 'preact', 'ember', 'alpine.js',
        'adonisjs', 'micronaut', 'quarkus', 'tornado', 'bottle'
    ],
    'DevOps et Infrastructure': [
        'docker', 'podman', 'cri-o', 'containerd', 'kubernetes', 'ci/cd', 'jenkins',
        'gitlab', 'github actions', 'tekton', 'drone ci', 'terraform', 'ansible',
        'chef', 'puppet', 'vagrant', 'devops', 'déploiement', 'intégration continue',
        'conteneur', 'orchestration', 'helm', 'argocd', 'circleci', 'travis', 'bamboo',
        'octopus deploy', 'spinnaker', 'gitops', 'infrastructure as code', 'iac',
        'monitoring', 'observabilité', 'prometheus', 'grafana', 'elk', 'splunk',
        'datadog', 'new relic', 'nagios', 'zabbix', 'pagerduty', 'elastic apm',
        'datadog synthetics', 'github actions self-hosted runners', 'mft', 'managed file transfer'
    ],
    'Cloud et Virtualisation': [
        'aws', 'azure', 'gcp', 'oracle cloud', 'alibaba cloud', 'digital ocean', 'hetzner cloud',
        'cloud', 'virtualbox', 'vmware', 'hyper-v', 'kvm', 'machine virtuelle',
        'iaas', 'paas', 'saas', 'lambda', 'ec2', 's3', 'cloudformation', 'sagemaker',
        'vertex ai', 'azure ml', 'openstack', 'proxmox', 'esxi', 'vcenter', 'citrix',
        'xen', 'cloud privé', 'cloud hybride', 'cloud public', 'multi-cloud',
        'azure devops', 'aws cloudwatch', 'elastic beanstalk', 'ecs', 'eks',
        'aks', 'gke', 'cloud run', 'app engine', 'cloud functions', 'knative',
        'openfaas', 'kubeless'
    ],
    'Bases de données': [
        'mysql', 'postgresql', 'mongodb', 'redis', 'cassandra', 'oracle', 'sql server',
        'sqlite', 'database', 'base de données', 'nosql', 'elasticsearch', 'dynamodb',
        'mariadb', 'neo4j', 'vector database', 'pinecone', 'weaviate', 'qdrant', 'chroma',
        'db2', 'sybase', 'firebird', 'couchdb', 'raven', 'influxdb', 'timescale',
        'cockroachdb', 'yugabyte', 'fauna', 'arangodb', 'orientdb', 'dgraph', 'tigergraph',
        'memcached', 'etcd', 'consul', 'apache hbase', 'apache phoenix',
        'hadoop hdfs', 'spark sql', 'delta lake', 'presto', 'druid', 'sql', 'plsql',
        'tsql', 'acid', 'cap', 'sharding', 'réplication', 'indexation', 'optimisation requêtes', 'tuning'
    ],
    'Communication et Soft Skills': [
        'communication', 'rédaction', 'documentation', 'présentation', 'collaboration',
        'travail d\'équipe', 'leadership', 'écoute', 'pédagogie', 'clarification',
        'adaptabilité', 'engagement', 'professionnelle', 'claire', 'technique',
        'vulgarisation', 'mentoring', 'coaching', 'gestion d\'équipe', 'management',
        'négociation', 'résolution de conflits', 'intelligence émotionnelle',
        'pensée critique', 'créativité', 'innovation', 'problem solving', 'prise de décision',
        'assertivité', 'empathie', 'public speaking', 'storytelling', 'active listening'
    ],
    'Sécurité informatique': [
        'cybersécurité', 'penetration testing', 'ethical hacking', 'firewall', 'vpn',
        'ids', 'ips', 'cryptographie', 'ssl', 'tls', 'authentification', 'mfa', 'sso',
        'auditing', 'forensic', 'siem', 'vulnerability management', 'patch management',
        'pentest', 'soc', 'cve', 'owasp top 10', 'mitre att&ck', 'burp suite',
        'metasploit', 'nmap', 'nessus', 'wireshark', 'hashcat'
    ],
    'Réseaux et Télécommunications': [
        'tcp/ip', 'udp', 'dns', 'dhcp', 'routing', 'switching', 'firewall', 'vpn',
        'lan', 'wan', 'wi-fi', 'ethernet', '5g', '4g', 'voip', 'mpls', 'bgp', 'ospf',
        'sip', 'rtp', 'lte', 'nr 5g', 'cisco', 'juniper', 'wireshark', 'iperf', 'ping',
        'traceroute', 'netcat'
    ],
    'Développement Web et Mobile': [
        'html', 'css', 'javascript', 'typescript', 'react', 'angular', 'vue', 'flutter',
        'swift', 'kotlin', 'react native', 'ionic', 'android', 'ios', 'responsive',
        'mobile', 'frontend', 'backend', 'fullstack', 'progressive web apps',
        'service worker', 'cordova', 'xamarin.forms', 'jetpack compose', 'swiftui'
    ],
    'APIs et Intégration': [
        'rest', 'rest api', 'graphql', 'soap', 'oauth', 'jwt', 'webhook', 'integration',
        'microservices', 'api design', 'api gateway'
    ],
    'Gestion de versions': [
        'git', 'github', 'gitlab', 'bitbucket', 'svn', 'mercurial', 'version control'
    ],
    'Testing et Qualité': [
        'unit testing', 'integration testing', 'e2e testing', 'selenium', 'cypress',
        'pytest', 'jest', 'mocha', 'tdd', 'bdd', 'qa', 'quality assurance',
        'code review', 'linting', 'static analysis', 'load testing', 'stress testing',
        'mutation testing', 'security testing', 'sonarqube', 'coverity', 'robot framework',
        'cucumber', 'pytest-bdd'
    ],
    'Analyse de données': [
        'data analysis', 'pandas', 'numpy', 'matplotlib', 'seaborn', 'plotly',
        'data visualization', 'data cleaning', 'data wrangling', 'statistics', 'r',
        'sql', 'excel', 'power bi', 'tableau', 'spark', 'hadoop', 'big data',
        'databricks', 'hue', 'airflow', 'prefect', 'luigi', 'polars', 'vaex',
        'bokeh', 'altair', 'dask'
    ],
    'Méthodologies et Frameworks de travail': [
        'agile', 'scrum', 'kanban', 'lean', 'waterfall', 'prince2', 'gestion de projet',
        'jira', 'trello', 'asana', 'microsoft project'
    ],
    'Blockchain et Web3': [
        'blockchain', 'ethereum', 'smart contract', 'solidity', 'web3', 'nft',
        'defi', 'cryptomonnaie', 'bitcoin', 'polkadot', 'cosmos', 'tezos', 'solana',
        'cardano', 'avalanche', 'hardhat', 'truffle', 'alchemy', 'moralis', 'ethers.js', 'web3.py'
    ],
    'IoT et Systèmes embarqués': [
        'iot', 'arduino', 'raspberry pi', 'esp32', 'beaglebone', 'particle', 'nrf52',
        'embedded', 'microcontroller', 'sensors', 'actuators', 'zigbee', 'mqtt',
        'coap', 'lora', 'zwave', 'edge computing', 'firmware'
    ],
    'ERP et Systèmes de gestion': [
        'sap', 'oracle ebs', 'dynamics', 'odoo', 'erp', 'gestion d\'entreprise'
    ],
    'Multimédia et Création': [
        'photoshop', 'illustrator', 'after effects', 'premiere pro', 'blender', 'maya',
        'cinema 4d', 'houdini', 'unreal engine', 'unity', '3d modeling', 'animation',
        'design', 'ui/ux', 'graphic design', 'video editing', 'sound design', 'audacity',
        'ableton', 'pro tools'
    ],
    'Automatisation et Scripting': [
        'bash', 'shell', 'powershell', 'python', 'rpa', 'robot framework', 'scripting',
        'automation', 'puppeteer', 'selenium', 'ansible', 'autohotkey', 'uiautomation',
        'blue prism', 'automation anywhere', 'power automate', 'perl', 'python scripting',
        'mft', 'managed file transfer'
    ],
    'Autres compétences': []
}

# Ordre de priorité pour l'affichage
ORDRE_PRIORITAIRE = [
    'Intelligence Artificielle et ML',
    'Architecture et Conception',
    'Langages de programmation',
    'Frameworks et bibliothèques',
    'DevOps et Infrastructure',
    'Cloud et Virtualisation',
    'Bases de données',
    'Réseaux et Télécommunications',
    'Systèmes et Administration',
    'Sécurité informatique',
    'Développement Web et Mobile',
    'APIs et Intégration',
    'Gestion de versions',
    'Testing et Qualité',
    'Analyse de données',
    'Méthodologies et Frameworks de travail',
    'Blockchain et Web3',
    'IoT et Systèmes embarqués',
    'ERP et Systèmes de gestion',
    'Communication et Soft Skills',
    'Multimédia et Création',
    'Automatisation et Scripting',
    'Autres compétences'
]


def categoriser_competence_automatique(competence: str) -> str:
    """
    Catégorise automatiquement une compétence dans un domaine.
    PRIORITÉ MAXIMALE: Détecter les compétences IA.
    """
    comp_lower = competence.lower()

    scores = {}
    for domaine, mots_cles in CATEGORIES.items():
        score = sum(1 for mot in mots_cles if mot in comp_lower)
        if score > 0:
            if domaine == 'Intelligence Artificielle et ML':
                scores[domaine] = score * 3
            else:
                scores[domaine] = score

    if scores:
        return max(scores.items(), key=lambda x: x[1])[0]

    return 'Autres compétences'


# Normalisation des domaines
NORMALISATION_DOMAINES = {
    'intelligence artificielle et ml': 'Intelligence Artificielle et ML',
    'intelligence artificielle': 'Intelligence Artificielle et ML',
    'ia et ml': 'Intelligence Artificielle et ML',
    'machine learning': 'Intelligence Artificielle et ML',
    'devops et infrastructure': 'DevOps et Infrastructure',
    'devops': 'DevOps et Infrastructure',
    'cloud et virtualisation': 'Cloud et Virtualisation',
    'cloud': 'Cloud et Virtualisation',
    'base de données': 'Bases de données',
    'bases de données': 'Bases de données',
    'database': 'Bases de données',
    'systèmes et administration': 'Systèmes et Administration',
    'système': 'Systèmes et Administration',
    'développement web et mobile': 'Développement Web et Mobile',
    'web et mobile': 'Développement Web et Mobile',
    'web': 'Développement Web et Mobile',
    'communication et soft skills': 'Communication et Soft Skills',
    'soft skills': 'Communication et Soft Skills',
    'gestion de versions': 'Gestion de versions',
    'version control': 'Gestion de versions',
    'apis et intégration': 'APIs et Intégration',
    'testing et qualité': 'Testing et Qualité',
    'méthodologies et frameworks de travail': 'Méthodologies et Frameworks de travail',
    'gestion de projet': 'Méthodologies et Frameworks de travail',
    'architecture et conception': 'Architecture et Conception',
    # Ajouts
    'intelligence artificielle avancée': 'Intelligence Artificielle et ML',
    'mlops': 'DevOps et Infrastructure',
    'monitoring': 'DevOps et Infrastructure',
    'big data': 'Analyse de données',
    'data science': 'Analyse de données',
    'frontend': 'Développement Web et Mobile',
    'backend': 'Développement Web et Mobile',
    'fullstack': 'Développement Web et Mobile',
    'blockchain': 'Blockchain et Web3',
    'smart contract': 'Blockchain et Web3',
    'web3': 'Blockchain et Web3',
    'iot': 'IoT et Systèmes embarqués'
}


def normaliser_domaine(domaine: str) -> str:
    """Normalise le nom d'un domaine."""
    domaine_lower = domaine.lower().strip()
    return NORMALISATION_DOMAINES.get(domaine_lower, domaine.strip())


# Normalisation des compétences
NORMALISATION_COMPETENCES = {
    'chatgpt': 'ChatGPT',
    'gpt-4': 'GPT-4',
    'gpt-3': 'GPT-3',
    'dall-e': 'DALL-E',
    'dall·e': 'DALL-E',
    'python': 'Python',
    'javascript': 'JavaScript',
    'typescript': 'TypeScript',
    'docker': 'Docker',
    'kubernetes': 'Kubernetes',
    'git': 'Git',
    'github': 'GitHub',
    'gitlab': 'GitLab',
    'linux': 'Linux',
    'aws': 'AWS',
    'azure': 'Azure',
    'gcp': 'GCP',
    'mysql': 'MySQL',
    'postgresql': 'PostgreSQL',
    'mongodb': 'MongoDB',
    'tensorflow': 'TensorFlow',
    'pytorch': 'PyTorch',
    'jenkins': 'Jenkins',
    'ansible': 'Ansible',
    'terraform': 'Terraform',
    'rest api': 'REST API',
    'api rest': 'REST API',
    'graphql': 'GraphQL',
    'oauth': 'OAuth',
    'jwt': 'JWT',
    'ci/cd': 'CI/CD',
    'devops': 'DevOps',
    'agile': 'Agile',
    'scrum': 'Scrum',
    'kanban': 'Kanban'
}


def normaliser_competence(comp: str) -> str:
    """Normalise le nom d'une compétence."""
    comp = comp.strip()
    comp = comp.rstrip('.,;:')
    comp_lower = comp.lower()
    return NORMALISATION_COMPETENCES.get(comp_lower, comp)
