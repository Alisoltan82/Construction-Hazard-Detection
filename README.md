🇬🇧 [English](./README.md) | 🇹🇼 [繁體中文](./README-zh-tw.md)

<img width="100%" src="./assets/images/project_graphics/banner.gif" alt="AI-Driven Construction Safety Banner">

<div align="center">
   <a href="examples/YOLO_server_api">Server-API</a> |
   <a href="examples/streaming_web">Streaming-Web</a> |
   <a href="examples/user_management">User-Management</a> |
   <a href="examples/YOLO_data_augmentation">Data-Augmentation</a> |
   <a href="examples/YOLO_evaluation">Evaluation</a> |
   <a href="examples/YOLO_train">Train</a>
</div>

<br>

<div align="center">
   <a href="https://www.python.org/downloads/release/python-3127/">
      <img src="https://img.shields.io/badge/python-3.12.7-blue?logo=python" alt="Python 3.12.7">
   </a>
   <a href="https://github.com/ultralytics/ultralytics">
      <img src="https://img.shields.io/badge/YOLO11-ultralytics-blue?logo=yolo" alt="YOLO11">
   </a>
   <a href="https://scikit-learn.org/stable/modules/generated/sklearn.cluster.HDBSCAN.html">
      <img src="https://img.shields.io/badge/HDBSCAN-sklearn-orange?logo=scikit-learn" alt="HDBSCAN sklearn">
   </a>
   <a href="https://flask.palletsprojects.com/en/3.0.x/">
      <img src="https://img.shields.io/badge/flask-3.0.3-blue?logo=flask" alt="Flask 3.0.3">
   </a>
   <a href="https://github.com/pre-commit/pre-commit">
      <img src="https://img.shields.io/badge/pre--commit-4.0.1-blue?logo=pre-commit" alt="Pre-commit 4.0.1">
   </a>
   <a href="https://docs.pytest.org/en/latest/">
      <img src="https://img.shields.io/badge/pytest-8.3.3-blue?logo=pytest" alt="pytest 8.3.3">
   </a>
   <a href="https://codecov.io/github/yihong1120/Construction-Hazard-Detection" >
      <img src="https://codecov.io/github/yihong1120/Construction-Hazard-Detection/graph/badge.svg?token=E0M66BUS8D" alt="Codecov">
   </a>
   <a href="https://codebeat.co/projects/github-com-yihong1120-construction-hazard-detection-main">
      <img alt="codebeat badge" src="https://codebeat.co/badges/383396a9-e2cb-4604-8990-c1707e5870cf" />
   </a>
</div>

<br>

"Construction-Hazard-Detection" is an AI-powered tool designed to enhance safety on construction sites. By leveraging the YOLO model for object detection, it identifies potential hazards such as:

- Workers without helmets
- Workers without safety vests
- Workers near machinery or vehicles
- Workers in restricted areas, restricted areas will be automatically generated by computing and clustering the coordinates of safety cones.

Post-processing algorithms further improve detection accuracy. The system is built for real-time deployment, offering instant analysis and alerts for identified hazards.

Additionally, the system integrates AI recognition results in real-time via a web interface. It can send notifications and real-time on-site images through messaging apps like LINE, Messenger, WeChat, and Telegram for prompt alerts and reminders. The system also supports multiple languages, enabling users to receive notifications and interact with the interface in their preferred language. Supported languages include:

- 🇹🇼 Traditional Chinese (Taiwan)
- 🇨🇳 Simplified Chinese (Mainland China)
- 🇫🇷 French
- 🇬🇧 English
- 🇹🇭 Thai
- 🇻🇳 Vietnamese
- 🇮🇩 Indonesian

This multi-language support makes the system accessible to a global audience, improving usability across different regions.

> **TODO**: Add support for WhatsApp notifications, and utilise Line Message API.

<br>
<br>

<div align="center">
   <img src="./assets/images/hazard-detection.png" alt="Hazard Detection Diagram" style="width: 100%;">
</div>

<br>

## Contents

- [Hazard Detection Examples](#hazard-detection-examples)
- [Usage](#usage)
- [Additional Information](#additional-information)
- [Dataset Information](#dataset-information)
- [Contributing](#contributing)
- [Development Roadmap](#development-roadmap)
- [License](#license)

## Hazard Detection Examples

Below are examples of real-time hazard detection by the system:

<div style="display: flex; justify-content: space-between; flex-wrap: wrap;">
  <!-- Example 1: Workers without Helmets or Safety Vests -->
  <div style="text-align: center; flex-basis: 33%;">
    <img src="./assets/images/demo/person_did_not_wear_safety_vest.png" alt="Workers without helmets or safety vests" style="width: 300px; height: 200px; object-fit: cover;">
    <p>Workers without Helmets or Safety Vests</p>
  </div>

  <!-- Example 2: Workers near Machinery or Vehicles -->
  <div style="text-align: center; flex-basis: 33%;">
    <img src="./assets/images/demo/person_near_machinery.jpg" alt="Workers near machinery or vehicles" style="width: 300px; height: 200px; object-fit: cover;">
    <p>Workers near Machinery or Vehicles</p>
  </div>

  <!-- Example 3: Workers in Restricted Areas -->
  <div style="text-align: center; flex-basis: 33%;">
    <img src="./assets/images/demo/persons_in_restricted_zones.jpg" alt="Workers in restricted areas" style="width: 300px; height: 200px; object-fit: cover;">
    <p>Workers in Restricted Areas</p>
  </div>
</div>

## Usage

Before running the application, you need to configure the system by specifying the details of the video streams and other parameters in a YAML configuration file. An example configuration file `configuration.yaml` should look like this:

```yaml
# This is a list of video configurations
- video_url: "rtsp://example1.com/stream"  # URL of the video
  site: "Construction Site"  # Location of the monitoring system
  stream_name: "Front Gate"  #  Number of the monitor
  model_key: "yolo11n"  # Model key for the video
  notifications:  # List of line tokens, and languages for notifications
    line_token_1: language_1
    line_token_2: language_2
  detect_with_server: True  # Run objection detection with server
  expire_date: "2024-12-31T23:59:59"  # Expire date in ISO 8601 format
- video_url: "streaming URL"  # Streaming URL of the video
  site: "Factory_1"  # Location of the monitoring system
  stream_name: "camera_1"  # Number of the monitor
  model_key: "yolo11n"  # Model key for detection
  notifications:  # List of line tokens, and languages for notifications
    line_token_3: language_3
    line_token_4: language_4
  detect_with_server: False  # Run objection detection in local
  expire_date: "No Expire Date"  # String for no expire date
```

Each object in the array represents a video stream configuration with the following fields:

- `video_url`: The URL of the live video stream. This can include:
   - Surveillance streams
   - RTSP streams
   - Secondary streams
   - YouTube videos or live streams
   - Discord streams
- `site`: TThe location of the monitoring system (e.g., construction site, factory).
- `stream_name`: The name assigned to the camera or stream (e.g., "Front Gate", "Camera 1").
- `model_key`: The key identifier for the machine learning model to use (e.g., "yolo11n").
- `notifications`: A list of LINE messaging API tokens and corresponding languages for sending notifications.
   - `line_token_1`, `line_token_2`, etc.: These are the LINE API tokens.
   - `language_1`, `language_2`, etc.: The languages for the notifications (e.g., "en" for English, "zh-TW" for Traditional Chinese). For information on how to obtain a LINE token, please refer to [line_notify_guide_en](docs/en/line_notify_guide_en.md).
- `line_token`: The LINE messaging API token for sending notifications.  For information on how to obtain a LINE token, please refer to [line_notify_guide_en](docs/en/line_notify_guide_en.md).
- `detect_with_server`: Boolean value indicating whether to run object detection using a server API. If `True`, the system will use the server for object detection. If `False`, object detection will run locally on the machine.
- `expire_date`: Expire date for the video stream configuration in ISO 8601 format (e.g., "2024-12-31T23:59:59"). If there is no expiration date, a string like "No Expire Date" can be used.

<br>

Now, you could launch the hazard-detection system in Docker or Python env:

<details>
   <summary>Docker</summary>

   ### Usage for Docker

   To run the hazard detection system, you need to have Docker and Docker Compose installed on your machine. Follow these steps to get the system up and running:

   1. Clone the repository to your local machine.
      ```
      git clone https://github.com/yihong1120/Construction-Hazard-Detection.git
      ```

   2. Navigate to the cloned directory.
      ```
      cd Construction-Hazard-Detection
      ```

   3. Build and run the services using Docker Compose:
      ```bash
      docker-compose up --build
      ```

   4. To run the main application with a specific configuration file, use the following command:
      ```bash
      docker-compose run main-application python main.py --config /path/in/container/configuration.yaml
      ```
      Replace `/path/in/container/configuration.yaml` with the actual path to your configuration file inside the container.

   5. To stop the services, use the following command:
      ```bash
      docker-compose down
      ```

</details>

<details>
   <summary>Python</summary>

   ### Usage for Python

   To run the hazard detection system with Python, follow these steps:

   1. Clone the repository to your local machine:
      ```bash
      git clone https://github.com/yihong1120/Construction-Hazard-Detection.git
      ```

   2. Navigate to the cloned directory:
      ```bash
      cd Construction-Hazard-Detection
      ```

   3. Install required packages:
      ```bash
      pip install -r requirements.txt
      ```

   4. Install and launch MySQL service (if required):

      For Ubuntu users:
      ```bash
      sudo apt install mysql-server
      sudo systemctl start mysql.service
      ```

      For others, you can download and install MySQL that works in your operation system in this [link](https://dev.mysql.com/downloads/).

   5. Start user management API:
      ```bash
      gunicorn -w 1 -b 0.0.0.0:8000 "examples.user_management.app:user-managements-app"
      ```

   6. Run object detection API:
      ```bash
      gunicorn -w 1 -b 0.0.0.0:8001 "examples.YOLO_server_api.app:app"
      ```

   7. Run the main application with a specific configuration file:
      ```bash
      python3 main.py --config /path/to/your/configuration.yaml
      ```
      Replace `/path/to/your/configuration.yaml` with the actual path to your configuration file.

   8. Start the streaming web service:

      For linux users:
      ```bash
      gunicorn -w 1 -k eventlet -b 127.0.0.1:8002 "examples.streaming_web.app:streaming-web-app"
      ```

      For windows users:
      ```
      waitress-serve --host=127.0.0.1 --port=8002 "examples.streaming_web.app:streaming-web-app"
      ```

</details>

## Additional Information

- The system logs are available within the Docker container and can be accessed for debugging purposes.
- The output images with detections (if enabled) will be saved to the specified output path.
- Notifications will be sent through LINE messaging API during the specified hours if hazards are detected.

### Notes

- Ensure that the `Dockerfile` is present in the root directory of the project and is properly configured as per your application's requirements.
- The `-p 8080:8080` flag maps port 8080 of the container to port 8080 on your host machine, allowing you to access the application via the host's IP address and port number.

For more information on Docker usage and commands, refer to the [Docker documentation](https://docs.docker.com/).

## Dataset Information

The primary dataset for training this model is the [Construction Site Safety Image Dataset from Roboflow](https://www.kaggle.com/datasets/snehilsanyal/construction-site-safety-image-dataset-roboflow/data). We have enriched this dataset with additional annotations and made it openly accessible on Roboflow. The enhanced dataset can be found here: [Construction Hazard Detection on Roboflow](https://universe.roboflow.com/side-projects/construction-hazard-detection). This dataset includes the following labels:

- `0: 'Hardhat'`
- `1: 'Mask'`
- `2: 'NO-Hardhat'`
- `3: 'NO-Mask'`
- `4: 'NO-Safety Vest'`
- `5: 'Person'`
- `6: 'Safety Cone'`
- `7: 'Safety Vest'`
- `8: 'Machinery'`
- `9: 'Vehicle'`

<details>
   <summary>Models for detection</summary>

   | Model   | size<br><sup>(pixels) | mAP<sup>val<br>50 | mAP<sup>val<br>50-95 | params<br><sup>(M) | FLOPs<br><sup>(B) |
   | ------- | --------------------- | ------------------ | ------------------ | ----------------- | ----------------- |
   | YOLO11n | 640                   | 54.1               | 31.0               | 2.6               | 6.5               |
   | YOLO11s | 640                   | //                 | //                 | 9.4               | 21.6              |
   | YOLO11m | 640                   | //                 | //                 | 20.1              | 68.0              |
   | YOLO11l | 640                   | //                 | //                 | 25.3              | 86.9              |
   | YOLO11x | 640                   | 76.8               | 52.5               | 56.9              | 194.9             |

</details>

<br>

Our comprehensive dataset ensures that the model is well-equipped to identify a wide range of potential hazards commonly found in construction environments.

## Contributing

We welcome contributions to this project. Please follow these steps:
1. Fork the repository.
2. Make your changes.
3. Submit a pull request with a clear description of your improvements.

## Development Roadmap

- [x] Data collection and preprocessing.
- [x] Training YOLO model with construction site data.
- [x] Developing post-processing techniques for enhanced accuracy.
- [x] Implementing real-time analysis and alert system.
- [x] Testing and validation in simulated environments.
- [x] Deployment in actual construction sites for field testing.
- [x] Ongoing maintenance and updates based on user feedback.

## License

This project is licensed under the [AGPL-3.0 License](LICENSE.md).
