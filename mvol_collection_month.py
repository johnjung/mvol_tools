import argparse
import json
import os
import re

from mvol_identifier import MvolIdentifier

class IIIFCollectionMonth:
  """Make a collection for a month of Campus Publications (mvol) data. 
     e.g. https://iiif-collection.lib.uchicago.edu/mvol/0004/mvol-0004-1930-01.json

  """

  def __init__(self, title, identifier, description, attribution, directory):
    self.title = title
    self.identifier = identifier
    self.description = description
    self.attribution = attribution
    self.directory = directory

    self.mvolidentifier = MvolIdentifier(self.identifier)
    self.year = self.mvolidentifier.get_year()
    self.month = self.mvolidentifier.get_month()

  def data(self):

    collection = {
      'label': self.title + ', ' + '-'.join(self.identifier.split('-')[2:]),
      '@id': self.mvolidentifier.collection_url(),
      '@context': 'https://iiif.io/api/presentation/2/context.json',
      '@type': 'sc:Collection',
      'description': self.description,
      'attribution': self.attribution,
      'viewingHint': 'individuals',
      'members': []
    }

    for entry in os.listdir(self.directory):
      if os.path.isdir(self.directory + "/" + entry) and re.match(r"^\d{4}$", entry):
        entry_identifier = '-'.join(self.identifier.split('-')[:3]) + '-' + entry
        entry_mvolidentifier = MvolIdentifier(entry_identifier)
        if entry_mvolidentifier.get_month() == self.month:
          collection['members'].append({
            'label': self.title + ', ' + entry_mvolidentifier.get_year_month_date(),
            '@id': entry_mvolidentifier.manifest_url(),
            '@type': 'sc:Manifest',
            'viewingHint': 'individuals'
          })

    return collection

if __name__ == '__main__':
 
  def mvol_month(s):
    r = re.compile(r"mvol-\d{4}-\d{4}-\d{2}")
    if not r.match(s):
      raise argparse.ArgumentTypeError
    return s

  parser = argparse.ArgumentParser()
  parser.add_argument("identifier", help="e.g. mvol-0004-1931-01", type=mvol_month)
  parser.add_argument("directory", help="e.g. /Volumes/webdav/...")
  args = parser.parse_args()

  if args.identifier.startswith('mvol-0004'):
    title = 'Daily Maroon'
    description = 'A newspaper produced by students of the University of Chicago. Published 1900-1942 and continued by the Chicago Maroon.'
  else:
    raise NotImplementedError

  print(
    json.dumps(
      IIIFCollectionMonth(
        title,
        args.identifier,
        description,
        'University of Chicago',
        args.directory).data(),
      indent=4,
      sort_keys=True))

