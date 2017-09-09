# enigma2-iptv-bouquet
Generate enigma2 bouquet of IPTV channels using XML bouquet definition

Usage:

```
./parse_bouquet.py bouquet.xml
```

See the sample `bouquet.xml` for the file format.

To add a channel to the genrated bouquet use the `Service` node.

It is possible to mix normal channles with imported IPTV channels in the same bouquet. To include normal channel specify the SID from the normal bouquet file in the `sid` attribute.

The name provided from the IPTV service can be overwritten in the generated bouquet with the `name` attribute.

The channel type can be specified with the `type` attribute (default: `19` for HDTV; use `1` for normal channels)

The SID of an existing SAT or Cable channel with the same content can be defined with the `sid` attribute. This allows to use the picon and the EPG of the original channel for the imported IPTV channel.

Use markers (with the `Marker` node) to separate channels from different IPTV providers.

Use groups (with the `Group` node) to import channels based on the `group` attribute in the channels XML file.

Parser for M3U files to generate the channels XML file comes next.
