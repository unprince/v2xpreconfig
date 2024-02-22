import os
from optparse import OptionParser

# https://asn1tools.readthedocs.io/en/latest
import asn1tools


class Asn1(object):
    def __init__(self):
        self._cwd = os.path.dirname(os.path.realpath(__file__))
        self._fname = os.path.join(self._cwd, 'v2x_r14_preconfig.asn')
        self._pdu = 'SL-V2X-Preconfiguration-r14'
        self._obj = None
        self._codec_xer = None
        self._codec_jer = None
        self._codec_gser = None
        self._codec_uper = None
        self._indent = 2

    def set_indent(self, indent):
        self._indent = int(indent)
    
    @property
    def codec_xer(self):
        if self._codec_xer is None:
            self._codec_xer = asn1tools.compile_files(self._fname, codec='xer')
        return self._codec_xer

    @property
    def codec_jer(self):
        if self._codec_jer is None:
            self._codec_jer = asn1tools.compile_files(self._fname, codec='jer')
        return self._codec_jer

    @property
    def codec_gser(self):
        if self._codec_gser is None:
            self._codec_gser = asn1tools.compile_files(self._fname, codec='gser')
        return self._codec_gser

    @property
    def codec_uper(self):
        if self._codec_uper is None:
            self._codec_uper = asn1tools.compile_files(self._fname, codec='uper')
        return self._codec_uper
        
    def decode(self, rule, infile):
        if rule == 'xer':
            self._obj = self.codec_xer.decode(self._pdu, infile)
        elif rule == 'gser':
            self._obj = self.codec_gser.decode(self._pdu, infile)
        elif rule == 'jer':
            self._obj = self.codec_jer.decode(self._pdu, infile)
        elif rule == 'uper':
            if os.path.isfile(infile):
                self._obj = self.codec_uper.decode(self._pdu, infile)
            else:
                self._obj = self.codec_uper.decode(self._pdu, bytearray.fromhex(infile))

    def encode(self, rule, outfile):
        obj = None
        if rule == 'xer':
            indent = None if self._indent == 0 else self._indent
            obj = self.codec_xer.encode(self._pdu, self._obj, indent=indent)
        elif rule == 'gser':
            indent = None if self._indent == 0 else self._indent
            obj = self.codec_gser.encode(self._pdu, self._obj, indent=indent)
        elif rule == 'jer':
            indent = None if self._indent == 0 else ' ' * self._indent
            obj = self.codec_jer.encode(self._pdu, self._obj, indent=indent)
        elif rule == 'uper':
            obj = self.codec_uper.encode(self._pdu, self._obj)
        if obj:
            if outfile:
                with open(outfile, 'wb') as f:
                    f.write(obj)
            elif rule == 'uper':
                print(obj.hex())
            else:
                print(obj.decode())

def create_parser():
    rules=('xer', 'jer', 'gser', 'uper')
    indent=('0', '2', '4')
    p = OptionParser(usage='v2xpreconfig [Options] <infile> [outfile]')
    p.add_option('-i', '--in-rule', dest='in_rule', 
        help='Options: {}, default: {}. Specifie the input file encoding rules.'.format(', '.join(rules), rules[0]),
        choices=rules, default=rules[0]
    )
    p.add_option('-o', '--out-rule', dest='out_rule', 
        help='Options: {}, default: {}. Specifie the output file encoding rules.'.format(', '.join(rules), rules[3]),
        choices=rules, default=rules[3]
    )
    p.add_option('--indent', dest='indent', 
        help='Options: {}, default: {}. Specifie the amount of indent of the text of output file.'.format(', '.join(indent), indent[1]),
        choices=indent, default=indent[1]
    )
    return p

def main():
    parser = create_parser()
    (options, args) = parser.parse_args()
    if len(args) > 0:
        asn1 = Asn1()
        if options.indent:
            asn1.set_indent(options.indent)
        asn1.decode(options.in_rule, args[0])
        asn1.encode(options.out_rule, None if len(args) == 1 else args[1])
