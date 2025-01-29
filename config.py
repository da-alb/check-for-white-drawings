import yaml
import datetime

def load_config(config_file="config.yaml"):
    """Loads configuration from a YAML file."""
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)

        # Gestione delle impostazioni della data
        if 'date_settings' in config:
            date_config = config['date_settings']
            if date_config.get('use_today', False):
                target_date = datetime.date.today()
            elif 'specific_date' in date_config:
                try:
                    target_date = datetime.date.fromisoformat(date_config['specific_date'])
                except ValueError:
                    print(f"Error: Invalid date format in 'specific_date'. Use landlab-MM-DD.")
                    return None
            elif 'days_offset' in date_config:
                target_date = datetime.date.today() + datetime.timedelta(days=date_config['days_offset'])
            else:
                print("Warning: No valid date settings found. Using default (today's date).")
                target_date = datetime.date.today()

            config['target_date'] = target_date

        return config

    except FileNotFoundError:
        print(f"Error: Configuration file '{config_file}' not found.")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML in '{config_file}': {e}")
        return None