#!/usr/bin/env python

import argparse
import time
import io
import humanfriendly
import lxml.etree
import xml.etree.ElementTree
import xml.sax
import xml.dom.minidom


def parse_with_lxml_etree(s, bytesio):
    lxml.etree.XML(s)


def parse_with_etree(s, bytesio):
    xml.etree.ElementTree.fromstring(s)


class MyContentHandler(xml.sax.handler.ContentHandler):
    def startElement(self, name, attrs):
        pass


def parse_with_sax(s, bytesio):
    handler = MyContentHandler()
    xml.sax.parseString(s, handler)


def parse_with_iterparse(s, bytesio):
    for x in xml.etree.ElementTree.iterparse(bytesio):
        pass


def parse_with_minidom(s, bytesio):
    xml.dom.minidom.parse(bytesio)


def main():
    parser = argparse.ArgumentParser(
        description='Compare performance of several Python XML parsing '
        'libraries.')

    parser.add_argument(
        'input_file', nargs='+',
        help='Input XML files to use for performance testing.')
    parser.add_argument(
        '--test-size', '-s', default=2**30, type = humanfriendly.parse_size,
        help='The amount of test input fed to each parser. Human friendly sizes '
        'are acceptable. Default to 1GiB.')

    args = parser.parse_args()

    print('Loading input files...')
    in_xml = []
    for filename in args.input_file:
        with open(filename, 'rb') as f:
            s = f.read()
            in_xml.append((s, io.BytesIO(s)))
    print('Loaded {} file(s) containing {} of test input.'.format(
        len(in_xml),
        humanfriendly.format_size(sum(len(s) for s, _ in in_xml))))

    alternatives = {
        'xml.dom.minidom': parse_with_minidom,
        'xml.etree.ElementTree': parse_with_etree,
        'xml.etree.ElementTree.iterparse': parse_with_iterparse,
        'xml.sax': parse_with_sax,
        'lxml.etree': parse_with_lxml_etree,
    }

    results = []

    for name, parse_func in alternatives.items():
        print('Testing:', name)
        parsed_bytes = 0
        start = time.monotonic()
        i = 0
        last_print = 0
        while parsed_bytes < args.test_size:
            s, bytesio = in_xml[i % len(in_xml)]
            bytesio.seek(0)
            parse_func(s, bytesio)
            parsed_bytes += len(s)
            i += 1

            if parsed_bytes - last_print > 100000000:
                print('   Parsed {} so far...'.format(
                    humanfriendly.format_size(parsed_bytes)))
                last_print = parsed_bytes
        end = time.monotonic()
        rate = parsed_bytes / (end - start)
        print('Parsed {} in {} seconds. Parse rate was {}ps.'.format(
            humanfriendly.format_size(parsed_bytes),
            humanfriendly.format_number(end - start),
            humanfriendly.format_size(rate)))
        results.append((name, rate))

    print('Results:')
    for name, rate in results:
        print('   {}: {}ps'.format(name, humanfriendly.format_size(rate)))

if __name__ == '__main__':
    main()
