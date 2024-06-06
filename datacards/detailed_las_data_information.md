 ### **X, Y, and Z**
 The X, Y, and Z values are stored as long integers. The X, Y, and Z values are used in conjunction
 with the scale values and the offset values to determine the coordinate for each point as described
 in the Public Header Block section.

 ### **Intensity**
 The Intensity value is the integer representation of the pulse return magnitude. This value is op
 tional and system specific. However, it should always be included if available. If Intensity is not
 included, this value must be set to zero.
 Intensity, when included, is always normalized to a 16 bit, unsigned value by multiplying the value
 by 65,536/(intensity dynamic range of the sensor). For example, if the dynamic range of the sensor
 is 10 bits, the scaling value would be (65,536/1,024). This normalization is required to ensure that
 data from different sensors can be correctly merged.
 For systems based on technology other than pulsed lasers, Intensity values may represent estimated
 relative reflectivity, rather than a direct measurement of pulse return magnitude, and may be derived
 from multiple sources.

 **Note**: Please note that the following four fields (Return Number, Number of Returns, Scan Direc
 tion Flag, and Edge of Flight Line) are bit fields within a single byte

### **Return Number**
**Note:**
 Recall that the Point Data Record Size can be greater than the minimum required for a PDRF. These extra bytes
 follow the standard Point Record fields and are described in the Extra Bytes VLR section.

 The Return Number is the pulse return number for a given output pulse. A given output laser pulse
 can have many returns, and they must be marked in sequence of return. The first return will have
 a Return Number of one, the second a Return Number of two, and so on up to five returns. The
 Return Number must be between 1 and the Number of Returns, inclusive.
 For systems unable to record multiple returns, the Return Number should be set to one, unless it is
 synthetically derived and the Synthetic Return Number Global Encoding bit is set.

### **Number of Returns (Given Pulse)**

 The Number of Returns is the total number of returns for a given pulse. For example, a laser data
 point may be return two (Return Number) within a total number of up to five returns.
 For systems unable to record multiple returns, the Number of Returns should be set to one, unless
 it is synthetically derived and the Synthetic Return Number Global Encoding bit is set.

### **Scan Direction Flag**

 The Scan Direction Flag denotes the direction in which the scanner mirror was traveling at the time
 of the output pulse. A bit value of 1 is a positive scan direction, and a bit value of 0 is a negative
 scan direction (where positive scan direction is a scan moving from the left side of the in-track
 direction to the right side and negative the opposite).
 For Aggregate Model Systems or if the measurement system does not include a rotational compo
nent, the Scan Direction Flag should be set to zero.

### **Classification**

This field represents the class attributes of a point. If a point has never been classified, this byte
 must be set to zero. The format for classification is a bit encoded field with the lower five bits used
 for the class and the three high bits used for flags. The bit definitions are listed in Table 8 and the
 classification values in table below.

| Classification Value (Bits 0:4) | Meaning                         |
|---------------------------------|---------------------------------|
| 0                               | Created, Never Classified       |
| 1                               | Unclassified                |
| 2                               | Ground                          |
| 3                               | Low Vegetation                  |
| 4                               | Medium Vegetation               |
| 5                               | High Vegetation                 |
| 6                               | Building                        |
| 7                               | Low Point (Noise)               |
| 8                               | Model Key-Point (Mass Point)    |
| 9                               | Water                           |
| 10                              | Reserved for ASPRS Definition   |
| 11                              | Reserved for ASPRS Definition   |
| 12                              | Overlap Points                 |
| 13-31                           | Reserved for ASPRS Definition   |

| Bit | Field Name     | Description                                                                                                           |
|-----|----------------|-----------------------------------------------------------------------------------------------------------------------|
| 0:4 | Classification | Standard ASPRS classification from 0 to 31 as defined in the classification table for legacy point formats (see Reserved Point Classes). |
| 5   | Synthetic      | If set, this point was created by a technique other than direct observation such as digitized from a photogrammetric stereo model or by traversing a waveform. Point attribute interpretation might differ from non-Synthetic points. Unused attributes must be set to the appropriate default value. |
| 6   | Key-Point      | If set, this point is considered to be a model key-point and therefore generally should not be withheld in a thinning algorithm. |
| 7   | Withheld       | If set, this point should not be included in processing (synonymous with Deleted).                                    |

**Note:** Note that bits 5, 6, and 7 are treated as flags and can be set or clear in any combination.
 For example, a point with bits 5 and 6 both set to one and the lower five bits set to 2 would be a
 Ground point that had been Synthetically collected and marked as a model Key-Point.

 **Note:** We are using both 0 and 1 as Unclassified to maintain compatibility with current popular classification software
 such as TerraScan. We extend the idea of classification value 1 to include cases in which data have been subjected to a
 classification algorithm but emerged in an undefined state. For example, data with class 0 is sent through an algorithm
 to detect man-made structures points that emerge without having been assigned as belonging to structures could be
 remapped from class 0 to class 1.
 3 Overlap Points are those points that were immediately culled during the merging of overlapping flight lines. In
 general, the Withheld bit should be set since these points are not subsequently classified.

### **Scan Angle Rank**

 The Scan Angle Rank is a signed one-byte integer with a valid range from-90 to +90. The Scan
 Angle Rank is the angle (rounded to the nearest integer in the absolute value sense) at which the
 laser point was output from the laser system including the roll of the aircraft. The scan angle is
 within 1 degree of accuracy from +90 to-90 degrees. The scan angle is an angle based on 0 degrees
 being nadir, and-90 degrees to the left side of the aircraft in the direction of flight.
 For Aggregate Model Systems, the Scan Angle Rank should be set to zero unless assigned from a
 component measurement.

### **User Data**

This field may be used at the user's discretion.

### **Point Source ID**

 This value indicates the source from which this point originated. A source is typically defined as a
 grouping of temporally consistent data, such as a flight line or sortie number for airborne systems,
 a route number for mobile systems, or a setup identifier for static systems. Valid values for this
 field are 1 to 65,535 inclusive. Zero is reserved as a convenience to system implementers.