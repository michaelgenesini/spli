### 1 Protocol Version Exchange
When the connection has been established, both sides MUST send an identification string.  This identification string MUST be

`SSH-protoversion-softwareversion SP comments CR LF`

Since the protocol being defined in this set of documents is version 2.0, the ’protoversion’ MUST be "2.0".  The ’comments’ string is OPTIONAL. If the ’comments’ string is included, a ’space’ character (denoted above as SP, ASCII 32) MUST separate the ’softwareversion’ and ’comments’ strings.  The identification MUST be terminated by a single Carriage Return (CR) and a single Line Feed (LF) character (ASCII 13 and 10, respectively). Implementers who wish to maintain compatibility with older, undocumented versions of this protocol may want to process the identification string without expecting the presence of the carriage return character for reasons described in Section 5 of this document.  The null character MUST NOT be sent. The maximum length of the string is 255 characters, including the Carriage Return and Line Feed. The part of the identification string preceding the Carriage Return and Line Feed is used in the Diffie-Hellman key exchange (see Section 8).

The server MAY send other lines of data before sending the version string.  Each line SHOULD be terminated by a Carriage Return and Line Feed.  Such lines MUST NOT begin with "SSH-", and SHOULD be encoded in ISO-10646 UTF-8 [RFC3629] (language is not specified). Clients MUST be able to process such lines.  Such lines MAY be silently ignored, or MAY be displayed to the client user.  If they are displayed, control character filtering, as discussed in [SSH-ARCH], SHOULD be used.  The primary use of this feature is to allow TCP- wrappers to display an error message before disconnecting. Both the ’protoversion’ and ’softwareversion’ strings MUST consist of printable US-ASCII characters, with the exception of whitespace characters and the minus sign (-). The ’softwareversion’ string is primarily used to trigger compatibility extensions and to indicate the capabilities of an implementation.  The ’comments’ string SHOULD contain additional information that might be useful in solving user problems.  As such, an example of a valid identification string is

`SSH-2.0-billsSSH_3.6.3q3<CR><LF>`

This identification string does not contain the optional ’comments’ string and is thus terminated by a CR and LF immediately after the ’softwareversion’ string. Key exchange will begin immediately after sending this identifier. All packets following the identification string SHALL use the binary packet protocol, which is described in Section 6.

...(Compatibility With Old SSH Versions)

### 2 Binary Packet Protocol
Each packet is in the following format:
   - **uint32**    packet_length
   - **byte**      padding_length
   - **byte[n1]**  payload; n1 = packet_length - padding_length - 1
   - **byte[n2]**  random padding; n2 = padding_length
   - **byte[m]**   mac (Message Authentication Code - MAC); m = mac_length

---

   - **packet_length**
      The length of the packet in bytes, not including ’mac’ or the’packet_length’ field itself.
   - **padding_length**
      Length of ’random padding’ (bytes).
   - **payload**
      The useful contents of the packet.  If compression has been negotiated, this field is compressed.  Initially, compression MUST be "none".
   - **random padding**
      Arbitrary-length padding, such that the total length of (packet_length || padding_length || payload || random padding) is a multiple of the cipher block size or 8, whichever is larger. There MUST be at least four bytes of padding.  The padding SHOULD consist of random bytes.  The maximum amount of padding is 255 bytes.
   - **mac**
      Message Authentication Code.  If message authentication has been negotiated, this field contains the MAC bytes. Initially, the MAC algorithm MUST be "none".

Note that the length of the concatenation of ’packet_length’, ’padding_length’, ’payload’, and ’random padding’ MUST be a multiple of the cipher block size or 8, whichever is larger.  This constraint MUST be enforced, even when using stream ciphers.  Note that the ’packet_length’ field is also encrypted, and processing it requires special care when sending or receiving packets.  Also note that the insertion of variable amounts of ’random padding’ may help thwart traffic analysis. The minimum size of a packet is 16 (or the cipher block size, whichever is larger) bytes (plus ’mac’).  Implementations SHOULD decrypt the length after receiving the first 8 (or cipher block size, whichever is larger) bytes of a packet.