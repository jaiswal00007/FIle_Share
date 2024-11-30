<body>
    <div style="text-align: center;">
        <h1>
             <img width="50" height="50" src="https://img.icons8.com/flat-round/50/share--v1.png" alt="share--v1" style="display: block; margin: 0 auto;">
            GetChat Desktop Application
        </h1>
    </div>
    <h2>Overview</h2>
    <p>
        GetChat is a desktop application designed for seamless communication and file sharing over a local network. 
        The application allows users to create a host or join an existing one to send messages and transfer files 
        with ease. Built with Python and Tkinter, GetChat is intuitive, lightweight, and perfect for LAN-based communication.
    </p>
    <h2>Key Features</h2>
    <ul>
        <li><strong>LAN-Based Communication:</strong> Chat and share files with multiple users over a local network.</li>
        <li><strong>Create or Join a Host:</strong> Easily create a host or join using the host's IP address.</li>
        <li><strong>Real-time Messaging:</strong> Send instant messages to connected users.</li>
        <li><strong>File Sharing:</strong> Upload and send files directly through the application.</li>
        <li><strong>Executable File:</strong> Run the application directly via the provided <code>GetChat.exe</code>.</li>
        <li><strong>Cross-Platform Support:</strong> Works on Windows, macOS, and Linux with Python installed.</li>
    </ul>
    <h2>Installation</h2>
    <h3>Option 1: Run the Executable File (Windows)</h3>
    <ol>
        <li>Navigate to the <code>dist/GetChat</code> directory.</li>
        <li>Double-click on <code>GetChat.exe</code> to launch the application.</li>
    </ol>
    <h3>Option 2: Run the Python Script</h3>
    <ol>
        <li>Ensure Python is installed on your system.</li>
        <li>Install the required dependencies by running:
            <pre><code>pip install -r requirements.txt</code></pre>
        </li>
        <li>Execute the Python script:
            <pre><code>python GetChat.py</code></pre>
        </li>
    </ol>
    <h2>Use Case</h2>
    <p>
        GetChat is perfect for quick communication and file sharing within a local network. Here's how it works:
    </p>
    <ol>
        <li><strong>Create a Host:</strong> One user starts a session by clicking the "Create Host" button.</li>
        <li><strong>Join the Host:</strong> Other users join the session by entering the host's IP address.</li>
        <li><strong>Multiple Connections:</strong> Multiple users can join the same host and communicate seamlessly.</li>
        <li><strong>Messaging and File Sharing:</strong> Users can:
            <ul>
                <li>Send real-time messages to the group.</li>
                <li>Upload and send files using the "Upload" and "Send File" buttons.</li>
            </ul>
        </li>
    </ol>
    <h2>Screenshots</h2>
    <p>Below are some screenshots to help you understand the application interface:</p>
    <h3>1. Home Screen</h3>
    <img src="0AC1B8A1-1A1D-4381-B5B8-8891DB3325D1.png" alt="Home Screen" width="600">
    <p>Description: The main dashboard where users can create or join a host.</p>
    <h3>2. Chat and File Sharing Interface</h3>
    <img src="BA9B973A-A355-4A53-A6F2-EF3D60F7B6A4.png" alt="Chat and File Sharing Interface" width="600">
    <p>Description: Interface for real-time messaging and file sharing between connected users.</p>
    <h2>Technologies Used</h2>
    <ul>
        <li><strong>Programming Language:</strong> Python</li>
        <li><strong>GUI Framework:</strong> Tkinter</li>
        <li><strong>Networking:</strong> Python <code>socket</code> module</li>
        <li><strong>File Handling:</strong> Python <code>os</code> and <code>shutil</code> modules</li>
        <li><strong>Executable Packaging:</strong> PyInstaller (for <code>.exe</code> file generation)</li>
    </ul>
    <h2>Future Improvements</h2>
    <ul>
        <li>Implement encryption for secure communication and file sharing.</li>
        <li>Improve the user interface for a modern and intuitive experience.</li>
        <li>Introduce a user authentication system for added security.</li>
        <li>Enable drag-and-drop file sharing functionality.</li>
        <li>Support audio and video calling over LAN.</li>
    </ul>
    <h2>Contributing</h2>
    <p>
        Contributions are welcome! If you have ideas or bug fixes, feel free to:
    </p>
    <ol>
        <li>Fork the repository.</li>
        <li>Create a new branch.</li>
        <li>Submit a pull request with a detailed description of your changes.</li>
    </ol>
    <h2>License</h2>
    <p>
        This project is licensed under the MIT License. See the <code>LICENSE</code> file for details.
    </p>
    <h2>Contact</h2>
    <p>
        Developed by <a href="mailto:anshujaiswal342@gmail.com">Anshu Jaiswal</a>.
    </p>
    <p>
        Feel free to open issues or suggest features in the repository's <strong>Issues</strong> section.
    </p>
</body>
