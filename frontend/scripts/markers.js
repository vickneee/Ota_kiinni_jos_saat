// This file contains functions to create and add markers to the map.
// The functions are used in the frontend/scripts/map.js file.
// The functions are used to create markers for criminals and investigators.
export async function createCriminalMarker(map, lat, lng) {
  try {
    const {AdvancedMarkerElement} = await google.maps.importLibrary('marker');
    const {PinElement} = await google.maps.importLibrary('marker');

    if (!PinElement) {
      throw new Error('PinElement is not available.');
    }

    const glyphImg1 = document.createElement('img');
    glyphImg1.src = '../assets/Karkuri.png';
    glyphImg1.style.width = '30px';
    glyphImg1.style.height = '30px';
    glyphImg1.classList.add('highlighted-image');
    glyphImg1.classList.add('hl-0');
    glyphImg1.title = 'Rikollinen';

    const glyphSvgPinElement1 = new PinElement({
      background: '#ffffff',
      glyph: glyphImg1,
      borderColor: '#C49339',
    });

    const glyphMarkerView1 = new AdvancedMarkerElement({
      map,
      position: {lat: lat, lng: lng},
      content: glyphSvgPinElement1.element,
      title: 'Rikollinen',
    });

    return glyphMarkerView1;
  } catch (error) {
    // console.error('Error creating criminal marker:', error);
  }
}

// Create and add the etsiva 1 marker
export async function createEtsijaMarker(map, lat, lng) {
  try {
    const {AdvancedMarkerElement} = await google.maps.importLibrary('marker');
    const {PinElement} = await google.maps.importLibrary('marker');
    const glyphImg2 = document.createElement('img');
    glyphImg2.src = '../assets/Etsiva_1.png';
    glyphImg2.style.width = '30px';  // Set the desired width
    glyphImg2.style.height = '30px';  // Set the desired height
    glyphImg2.classList.add('highlighted-image');  // Add a class to the element
    glyphImg2.classList.add('hl-1');  // Add a class to the element
    glyphImg2.title = 'Etsivä 1';

    const glyphSvgPinElement2 = new PinElement({
      background: '#ffffff',
      glyph: glyphImg2,
      borderColor: '#C49339',
    });

    const glyphMarkerView2 = new AdvancedMarkerElement({
      map,
      position: {lat: lat, lng: lng},
      content: glyphSvgPinElement2.element,
      title: 'Etsivä 1',
    });
    return glyphMarkerView2;
  } catch (error) {
    // console.error('Error creating etsiva 2 marker:', error);
  }
}

// Create and add the etsiva 2 marker
export async function createEtsija2Marker(map, lat, lng) {
  try {

    const {AdvancedMarkerElement} = await google.maps.importLibrary('marker');
    const {PinElement} = await google.maps.importLibrary('marker');
    const glyphImg2 = document.createElement('img');
    glyphImg2.src = '../assets/Etsiva_2.png';
    glyphImg2.style.width = '30px';  // Set the desired width
    glyphImg2.style.height = '30px';  // Set the desired height
    glyphImg2.classList.add('highlighted-image');  // Add a class to the element
    glyphImg2.classList.add('hl-2');  // Add a class to the element
    glyphImg2.title = 'Etsivä 2';

    const glyphPinElement3 = new PinElement({
      background: '#ffffff',
      glyph: glyphImg2,
      borderColor: '#C49339',
    });

    const glyphMarkerView3 = new AdvancedMarkerElement({
      map,
      position: {lat: lat, lng: lng},
      content: glyphPinElement3.element,
      title: 'Etsivä 2',
    });
    return glyphMarkerView3;
  } catch (error) {
    // console.error('Error creating etsiva 2 marker:', error);
  }
}

// Create and add the marker to the map
export function addMarkersToMap(map,recommendedAirports) {
  return new Promise(async (resolve, reject) => {
    try {
      let markers = [];
      let markersdata = [];
      // const players = playerData();
      // console.log(players);

      for (const airport of Object.values(recommendedAirports)) {
        const {AdvancedMarkerElement} = await google.maps.importLibrary('marker');
        const {PinElement} = await google.maps.importLibrary('marker');

        const pinType = determinePinType(airport.ticket_type);

        const pinElement = new PinElement({
          background: pinType, // Customize the pin color as needed
          glyphColor: airport.ticket_type === 'unknown' ? '#23245c' : '#C49339',
          borderColor: '#C49339',
        });

        const marker = new AdvancedMarkerElement({
          map: map,
          position: {lat: airport.latitude, lng: airport.longitude},
          content: pinElement.element,
          title: airport.icao,
        });

        marker.pinType = pinType;
        markers.push(marker);
        markersdata.push({'position': marker.position, 'title': marker.title});
      }
      console.log(markersdata);
      resolve({markers, markersdata});
    } catch (error) {
      reject(error);
    }
  });
}

// Determine the pin type based on the ticket type
export function determinePinType(ticketType) {
  // Define your criteria to determine the pin type based on the ticket type
  if (ticketType === 'potkurikone') {
    return 'red';
  } else if (ticketType === 'matkustajakone') {
    return 'blue';
  } else if (ticketType === 'yksityiskone') {
    return 'green';
  } else {
    return 'white';
  }
}

// Get the pin element based on the pin type
export function getPinElement(PinElement, type) {
  switch (type) {
    case 'green':
      return new PinElement({
        background: 'green',
        glyphColor: '#C49339',
        borderColor: '#C49339',
      });
    case 'red':
      return new PinElement({
        background: 'red',
        glyphColor: '#C49339',
        borderColor: '#C49339',
      });
    case 'blue':
      return new PinElement({
        background: 'blue',
        glyphColor: '#C49339',
        borderColor: '#C49339',
      });
    case 'white':
      return new PinElement({
        background: '#ffffff',
        glyphColor: '#23245c',
        borderColor: '#C49339',
      });
    default:
      return new PinElement({
        background: '#ffffff',
        glyphColor: '#23245c',
        borderColor: '#C49339',
      });
  }
}