import init_db
import asyncio

def main():
	asyncio.run(init_db.initialize_database())

if __name__ == "__main__":
	main()
