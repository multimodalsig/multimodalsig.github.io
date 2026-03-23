---
layout: research
title: Themes
permalink: /research/themes/
description: >
  Active research themes in the Multimodal Spatial Imaging Lab.
nav: false
---

Our research program is organized around five interconnected themes, unified
by a common foundation in **imaging metrology** — the science of extracting
precise, reliable geometric information from imaging sensors.

## Sensor Calibration & System Modelling

{: #calibration}

Imaging sensors are imperfect instruments. Terrestrial laser scanners exhibit
systematic errors in range, horizontal angle, and vertical angle measurements.
Cameras suffer from lens distortions. Range cameras have depth-dependent biases.
Our lab develops **rigorous mathematical models** of these error sources and
**self-calibration** procedures that estimate and mitigate them without
requiring dedicated calibration facilities.

Key contributions include:

- Comprehensive additional parameter models for terrestrial laser scanners
  (angular encoder errors, rangefinder offsets, axis misalignments)
- Correlation analysis between systematic error parameters and methods for
  their mitigation
- Self-calibration network design principles for TLS
- Kinect / PrimeSense 3D camera geometric calibration via bundle adjustment
- Spinning-beam LiDAR (Velodyne) calibration for mobile mapping

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod
tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
veniam, quis nostrud exercitation ullamco laboris.

## Structural Deformation Monitoring

{: #deformation}

Terrestrial laser scanners can measure millions of surface points in minutes,
but their single-point precision (typically ±2–25 mm) is often insufficient
for structural monitoring applications. Our lab has demonstrated that by
fitting **physically-motivated surface models** — beam deflection equations,
shell models, polynomial surfaces — to dense point clouds, deformation can
be measured at **6–20× better** than the raw point precision.

Applications include:

- Reinforced concrete beam load testing
- Bridge deck deflection monitoring
- Dam surface deformation
- Industrial pipe and vessel dimensional control

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis aute irure
dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat
nulla pariatur.

## Cultural Heritage Documentation

{: #heritage}

At-risk cultural heritage sites require rapid, accurate, and complete
three-dimensional documentation. Our lab applies terrestrial laser scanning
and close-range photogrammetry to record heritage structures across Alberta
and internationally.

Key projects include:

- Digitally Preserving Alberta's Diverse Cultural Heritage (with Dr. Peter
  Dawson, Anthropology & Archaeology)
- Herschel Island–Qikiqtaruk Territorial Park, Yukon
- Historic Ayutthaya, Thailand
- Brooks Aqueduct National Historic Site

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Excepteur sint
occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit
anim id est laborum.

## Biomedical Imaging Metrology

{: #biomedical}

Dual fluoroscopic imaging systems capture X-ray image pairs of human joints
during dynamic activities (walking, stair climbing) to measure in-vivo
kinematics. Our lab develops the **geometric calibration** and
**self-calibrating bundle adjustment** methods that underpin the accuracy
of these measurements.

Applications:

- Knee joint kinematics for orthopaedic research
- Surgical instrument tracking (C-arm pose estimation)
- Intramedullary nail pose recognition

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ut perspiciatis
unde omnis iste natus error sit voluptatem accusantium doloremque laudantium.

## Industrial Metrology & As-Built Modelling

{: #industrial}

Precision dimensional control in industrial environments — refineries,
processing plants, manufacturing facilities — demands accurate as-built
3D models derived from laser scanning and photogrammetric surveys. Our lab
develops automated methods for:

- Pipe spool recognition and dimensional extraction
- Object recognition and segmentation in industrial point clouds
- Automated progress reporting from smartphone imagery
- Quality assessment of mobile mapping system data

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nemo enim ipsam
voluptatem quia voluptas sit aspernatur aut odit aut fugit.
