# Last Night's Sunset 🌅

**Never miss the sunset again.** An automated system that captures, scores, and displays the best sunset photo from the previous night using computer vision and a Raspberry Pi.

See the project at [thesunset.austinsteinhart.com](thesunset.austinsteinhart.com).


## Overview

This project automatically captures sunset photos every day, scores them using computer vision algorithms, selects the best image, and displays it on a beautiful web interface. The system runs on a Raspberry Pi with a camera module and includes a responsive Svelte frontend for viewing sunset data.

## Features

- **Automated Daily Capture**: Takes photos every 5 minutes from 20 minutes before to 20 minutes after sunset
- **Computer Vision Scoring**: Uses color analysis and sunset-specific metrics to identify the best photo
- **Interactive Calendar**: Browse sunset photos by date with color-coded quality indicators
- **Data Visualization**: D3.js charts showing sunset quality scores over time
- **Responsive Design**: Mobile-friendly interface with smooth interactions
- **Cloud Storage**: Automatic upload to AWS S3 with metadata
- **Highlights Section**: Showcases the best recent sunsets

## Architecture

### Backend (Raspberry Pi)
- **Image Capture**: Python script using `picamera` or `opencv`
- **Sunset Timing**: `astral` library for accurate sunset calculations
- **Scheduling**: `schedule` library for automated daily execution
- **Computer Vision**: `OpenCV` and `Pillow` for image analysis
- **Cloud Upload**: `boto3` for AWS S3 integration

### Frontend (Web App)
- **Framework**: SvelteKit with TypeScript
- **Styling**: Custom CSS with responsive design
- **Data Visualization**: D3.js for interactive charts
- **Date Handling**: `date-fns` for date formatting and manipulation
- **Deployment**: Static hosting (Heroku/GitHub Pages)