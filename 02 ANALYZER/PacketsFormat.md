### 1 Protocol Version Exchange
When the connection has been established, both sides MUST send an identification string.  This identification string MUST be

`SSH-protoversion-softwareversion SP comments CR LF`

Since the protocol being defined in this set of documents is version 2.0, the ’protoversion’ MUST be "2.0".  The ’comments’ string is OPTIONAL. If the ’comments’ string is included, a ’space’ character (denoted above as SP, ASCII 32) MUST separate the ’softwareversion’ and ’comments’ strings.  The identification MUST be terminated by a single Carriage Return (CR) and a single Line Feed (LF) character (ASCII 13 and 10, respectively). Implementers who wish to maintain compatibility with older, undocumented versions of this protocol may want to process the identification string without expecting the presence of the carriage return character for reasons described in Section 5 of this document.  The null character MUST NOT be sent. The maximum length of the string is 255 characters, including the Carriage Return and Line Feed. The part of the identification string preceding the Carriage Return and Line Feed is used in the Diffie-Hellman key exchange (see Section 8).

The server MAY send other lines of data before sending the version string.  Each line SHOULD be terminated by a Carriage Return and Line Feed.  Such lines MUST NOT begin with "SSH-", and SHOULD be encoded in ISO-10646 UTF-8 [RFC3629]  (language is not specified). Clients MUST be able to process such lines.  Such lines MAY be silently ignored, or MAY be displayed to the client user.  If they are displayed, control character filtering, as discussed in [SSH-ARCH], SHOULD be used.  The primary use of this feature is to allow TCP- wrappers to display an error message before disconnecting. Both the ’protoversion’ and ’softwareversion’ strings MUST consist of printable US-ASCII characters, with the exception of whitespace characters and the minus sign (-). The ’softwareversion’ string is primarily used to trigger compatibility extensions and to indicate the capabilities of an implementation.  The ’comments’ string SHOULD contain additional information that might be useful in solving user problems.  As such, an example of a valid identification string is

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

...(Maximum Packet Length, Compression, Encryption, Data Integrity, Key Exchange Methods, Public Key Algorithms)

### 3 Key Exchange
Key exchange (kex) begins by each side sending name-lists of supported algorithms.  Each side has a preferred algorithm in each category, and it is assumed that most implementations, at any given time, will use the same preferred algorithm. Each side MAY guess which algorithm the other side is using, and MAY send an initial key exchange packet according to the algorithm, if appropriate for the preferred method.

...(Algorithm Negotiation, Output from Key Exchange, Taking Keys Into Use)

### 4 Algorithm Negotiation
Key exchange begins by each side sending the following packet:

 - **byte**    SSH_MSG_KEXINIT
 - **byte[16]**      cookie (random bytes)
 - **name-lists**    kex_algorithms
 - **name-list**     server_host_key_algorithms
 - **name-list**     encryption_algorithms_client_to_server
 - **name-list**     encryption_algorithms_server_to_client
 - **name-list**     mac_algorithms_client_to_server
 - **name-list**     mac_algorithms_server_to_client
 - **name-list**     compression_algorithms_client_to_server
 - **name-list**     compression_algorithms_server_to_client
 - **name-list**     languages_client_to_server
 - **name-list**     languages_server_to_client
 - **boolean**       first_kex_packet_follows
 - **uint32**        0 (reserved for future extension)

### 5 Diffie-Hellman Key Exchange [RFC4419]

First, the client sends:
 - **byte**    SSH_MSG_KEY_DH_GEX_REQUEST
 - **uint32**  min, minimal size in bits of an acceptable group
 - **uint32**  n, preferred size in bits of the group the server will send
 - **uint32**  max, maximal size in bits of an acceptable group

The server responds with
 - **byte**    SSH_MSG_KEX_DH_GEX_GROUP
 - **mpint**   p, safe prime
 - **mpint**   g, generator for subgroup in GF(p)

The client responds with:
 - **byte**    SSH_MSG_KEX_DH_GEX_INIT
 - **mpint**   e

The server responds with:
 - **byte**    SSH_MSG_KEX_DH_GEX_REPLY
 - **string**    server public host key and certificates (K_S)
 - **mpint**     f
 - **string**    signature of H

The hash H is computed as the HASH hash of the concatenation of the following:
 - **string**     V_C, the client’s version string (CR and NL excluded)
 - **string**     V_S, the server’s version string (CR and NL excluded)
 - **string**     I_C, the payload of the client’s SSH_MSG_KEXINIT
 - **string**     I_S, the payload of the server’s SSH_MSG_KEXINIT
 - **string**     K_S, the host key
 - **uint32**     min, minimal size in bits of an acceptable group
 - **uint32**     n, preferred size in bits of the group the server will send
 - **uint32**     max, maximal size in bits of an acceptable group
 - **mpint**      p, safe prime
 - **mpint**      g, generator for subgroup
 - **mpint**      e, exchange value sent by the client
 - **mpint**      f, exchange value sent by the server
 - **mpint**      K, the shared secret

 This value is called the exchange hash, and it is used to authenticate the key exchange as per [RFC4253].

######4. Key Exchange Methods
This document defines two new key exchange methods:

`"diffie-hellman-group-exchange-sha1" and "diffie-hellman-group-exchange-sha256"`.

######4.1. diffie-hellman-group-exchange-sha1
The "diffie-hellman-group-exchange-sha1" method specifies Diffie-Hellman Group and Key Exchange with SHA-1 [FIPS-180-2] as HASH.

######4.2. diffie-hellman-group-exchange-sha256
The "diffie-hellman-group-exchange-sha256" method specifies Diffie-Hellman Group and Key Exchange with SHA-256 [FIPS-180-2] as HASH.
Note that the hash used in key exchange (in this case, SHA-256) must also be used in the key derivation pseudo-random function (PRF), as per the requirement in the "Output from Key Exchange" section in [RFC4253].

######5. Summary of Message Numbers
The following message numbers have been defined in this document.
They are in a name space private to this document and not assigned by IANA.
 - #define SSH_MSG_KEX_DH_GEX_REQUEST_OLD  30
 - #define SSH_MSG_KEX_DH_GEX_REQUEST      34
 - #define SSH_MSG_KEX_DH_GEX_GROUP        31
 - #define SSH_MSG_KEX_DH_GEX_INIT         32
 - #define SSH_MSG_KEX_DH_GEX_REPLY        33

SSH_MSG_KEX_DH_GEX_REQUEST_OLD is used for backward compatibility.
Instead of sending "min || n || max", the client only sends "n". In addition, the hash is calculated using only "n" instead of "min || n || max". The numbers 30-49 are key exchange specific and may be redefined by other kex methods.