import os

def main():
    print("==== Smart Screen Controller ====")
    print("==== Developed by Saquib Nazeer ====")
    print("1. 🖐️ Start Gesture Controller")
    print("2. 🎤 Start Voice Controller")
    print("3. ❌ Exit")

    choice = input("Enter your choice (1/2/3): ").strip()

    if choice == "1":
        print("Starting Gesture Controller...")
        os.system("python gesture_controller.py")
    elif choice == "2":
        print("Starting Voice Controller...")
        os.system("python voice_controller.py")
    else:
        print("Exiting...")

if __name__ == "__main__":
    main()
