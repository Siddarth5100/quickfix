### Quickfix

Service Management system for mobile and laptop repair buisness

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app quickfix
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/quickfix
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit
### -------------------------------QuickFix-------------------------------
### Multi-site & Configuration

### Que: 
Explain in 4 sentences: what each config file is for and what breaks if you accidentally put a secret in common_site_config.json

### Ans:

### site_config.json : 
- Site level configuration
- Works only for that particular site
- It contains values like db name, pwd, type, key
- Exist in sites folder -> specific site folder

### common_site_config.json :
- Global (bench level) configuration
- Works for all site in the bench
- If something want to use commonly can mention here, not required to mention separately for each site
- Anything is placed here will affect all the sites as it is shared one
- It contails reidis config, global settings, bg services etc
- Exist inside sites folder

- As common_site_config is common, if serect key adds here all the other sites gets access easily which is not secure way


### Que:
4 processes bench start launches (web, worker, scheduler,
socketio) and explain what happens to background jobs if the worker process
crashes.

### Ans:
- redis_cache
- redis_queue
- web
- watch
- socketio

- If Worker gets crashed jobs will get queued when the worker resumes backgroud job will gets started
