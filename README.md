# amul-order

This project provides a simple Python script to automate ordering Amul lactose free milk once a week from [shop.amul.com](https://shop.amul.com/).

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `config.yaml` file using the provided template and fill in your credentials, shipping address and card details.
   **Keep this file secure and do not commit personal information to version control.**

## Running

Execute the scheduler:
```bash
python amul_order.py
```
The script uses a cron expression defined in `config.yaml` (`schedule.cron`) to determine when to place the order. By default it runs every Monday at 9 AM.

### Testing without the scheduler

If you just want to test the automation once without enabling the cron loop, use
the `--once` flag:

```bash
python amul_order.py --once
```

This runs the login, cart, and checkout steps once and then exits.

The HTTP endpoints used here are placeholders. You may need to update them according to the actual API offered by Amul.
