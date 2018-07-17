import argparse
import csv
import json
import os
import re   

import xml.etree.ElementTree as ElementTree

from mvol_identifier import MvolIdentifier

class IIIFManifest:
  """Make a manifest for a Campus Publications (mvol) issue.
     e.g. https://iiif-manifest.lib.uchicago.edu/mvol/0004/1929/0103/mvol-0004-1929-0103.json

  """

  def __init__(self, title, identifier, description, attribution, directory):

    self.title = title
    self.identifier = identifier
    self.description = description
    self.attribution = attribution
    self.directory = directory

    self.mvolidentifier = MvolIdentifier(self.identifier)
    self.year = self.mvolidentifier.get_year()

    self.struct_data = None
    self.mets_data = None
    self.namespaces = {
      "mets": "http://www.loc.gov/METS/",
      "mix": "http://www.loc.gov/mix/v20"
    }

  def _load_struct(self):
    self.struct_data = []
    with open(self.directory + '/' + self.identifier + '.struct.txt', 'r') as f:
      r = csv .reader(f, delimiter='\t')
      for row in r:
        if row[0] == 'object':
          continue
        self.struct_data.append(row)

  def get_page(self, n):
    if not self.struct_data:
      self._load_struct()
    return self.struct_data[n][1]

  def _load_mets(self):
    with open(self.directory + '/' + self.identifier + '.mets.xml', 'r') as f:
     self.mets_data = ElementTree.parse(f)

  def get_width(self, n):
    if not self.mets_data:
      self._load_mets()
    return int(self.mets_data.find('mets:amdSec/mets:techMD[' + str(n + 1) + ']/mets:mdWrap/mets:xmlData/mix:mix/mix:BasicImageInformation/mix:BasicImageCharacteristics/mix:imageWidth', self.namespaces).text)

  def get_height(self, n):
    if not self.mets_data:
      self._load_mets()
    return int(self.mets_data.find('mets:amdSec/mets:techMD[' + str(n + 1) + ']/mets:mdWrap/mets:xmlData/mix:mix/mix:BasicImageInformation/mix:BasicImageCharacteristics/mix:imageHeight', self.namespaces).text)

  def get_s3_directory(self):
    return 'https://s3.lib.uchicago.edu/owncloud/index.php/apps/files/?dir=/IIIF_Files/' + self.identifier.replace('-', '/') + '/JPEG'

  def data(self):
    manifest = {
      '@context': 'http://iiif.io/api/presentation/2/context.json',
      '@id': self.mvolidentifier.manifest_url(),
      '@type': 'sc:Manifest',
      'metadata': [
        {
          'label': 'Title',
          'value': self.title
        },
        {
          'label': 'Identifier',
          'value': self.identifier
        },
        {
          'label': 'Date',
          'value': self.mvolidentifier.get_year_month_date()
        }
      ],
      'description': self.description,
      'logo': 'https://www.lib.uchicago.edu/static/base/images/color-logo.png',
      'license': 'http://campub.lib.uchicago.edu/rights/',
      'attribution': 'University of Chicago Library',
      'label': self.title + ', ' + self.mvolidentifier.get_year_month_date(),
      'sequences': [
        {
          '@id': self.mvolidentifier.sequence_url(),
          '@type': 'sc:Sequence',
          'canvases': [],
        }
      ],
      'structures': [],
      'viewingDirection': 'left-to-right'
    }

    for e, entry in enumerate(os.listdir(self.directory + '/JPEG/')):
       manifest['sequences'][0]['canvases'].append({
        '@id': self.mvolidentifier.sequence_url(),
        '@type': 'sc:Canvas',
        'label': 'Page ' + self.get_page(e),
        'height': self.get_height(e),
        'width': self.get_width(e),
        'images': [
          {
            '@context': 'http://iiif.io/api/presentation/2/context.json',
            '@id': self.get_s3_directory(),
            '@type': 'oa:Annotation',
            'motivation': 'sc:Painting',
            'resource': {
              '@id': self.get_s3_directory(),
              '@type': 'dctypes:Image',
              'format': 'image/jpeg',
              'height': self.get_height(e),
              'width': self.get_width(e),
              'service': {
                '@context': 'http://iiif.io/api/image/2/context.json',
                '@id': self.get_s3_directory(),
                'profile': [
                   'http://iiif.io/api/image/2/level2.json',
                   {
                     'supports': [
                        'canonicalLinkHeader',
                        'profileLinkHeader',
                        'mirroring',
                        'rotationArbitrary',
                        'regionSquare',
                        'sizeAboveFull'
                     ],
                     'qualities': [
                       'default',
                       'gray',
                       'bitonal'
                     ],
                     'format': [
                       'jpg',
                       'png',
                       'gif',
                       'webp'
                      ]
                   }
                ]
              }
            },
            'on': self.mvolidentifier.manifest_url(),
          }
        ]
      })

    return manifest

if __name__ == '__main__':

  def mvol_year_month_date(s):
    r = re.compile(r"^mvol-\d{4}-\d{4}-\d{4}$")
    if not r.match(s):
      raise argparse.ArgumentTypeError
    return s

  parser = argparse.ArgumentParser()
  parser.add_argument("identifier", help="e.g. mvol-0004-1931", type=mvol_year_month_date)
  parser.add_argument("directory", help="e.g. /Volumes/webdav/...")
  args = parser.parse_args()

  if args.identifier.startswith('mvol-0004'):
    title = 'Daily Maroon'
    description = 'A newspaper produced by students of the University of Chicago published 1900-1942 and continued by the Chicago Maroon.'
  else:
    raise NotImplementedError

  print(
    json.dumps(
      IIIFManifest(
        title,
        args.identifier,
        description,
        'University of Chicago Library',
        args.directory).data(),
      indent=4,
      sort_keys=True))