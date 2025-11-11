// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract AlignCardNFT is ERC721, Ownable {
    mapping(address => bool) public minted;
    uint256 public nextId = 1;
    address public signer; // backend signer that attests wallet/tokenId/seed/gameId
    uint256 public currentGameId;

    // EIP-712
    bytes32 public immutable DOMAIN_SEPARATOR;
    bytes32 public constant TYPEHASH = keccak256(
        "AlignCard(address wallet,uint256 tokenId,bytes32 seed,uint256 gameId)"
    );

    event CardMinted(address indexed wallet, uint256 indexed tokenId, bytes32 seed, uint256 gameId);

    constructor(address _signer) ERC721("ALIGN Card","ALIGN") {
        signer = _signer;
        uint256 chainId;
        assembly { chainId := chainid() }
        DOMAIN_SEPARATOR = keccak256(abi.encode(
            keccak256("EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)"),
            keccak256(bytes("AlignCardNFT")),
            keccak256(bytes("1")),
            chainId,
            address(this)
        ));
    }

    function setSigner(address s) external onlyOwner { signer = s; }
    function setGame(uint256 gameId) external onlyOwner { currentGameId = gameId; }

    function mint(bytes32 seed, bytes calldata sig) external {
        require(!minted[msg.sender], "Already minted");
        uint256 tokenId = nextId++;

        // digest over (wallet, tokenId, seed, currentGameId)
        bytes32 digest = keccak256(abi.encodePacked(
            "\x19\x01",
            DOMAIN_SEPARATOR,
            keccak256(abi.encode(TYPEHASH, msg.sender, tokenId, seed, currentGameId))
        ));
        require(_recover(digest, sig) == signer, "Bad signature");

        minted[msg.sender] = true;
        _safeMint(msg.sender, tokenId);
        emit CardMinted(msg.sender, tokenId, seed, currentGameId);
    }

    function _recover(bytes32 hash, bytes memory signature) internal pure returns (address) {
        if (signature.length != 65) return address(0);
        bytes32 r; bytes32 s; uint8 v;
        assembly {
          r := mload(add(signature, 32))
          s := mload(add(signature, 64))
          v := byte(0, mload(add(signature, 96)))
        }
        if (v < 27) v += 27;
        return ecrecover(hash, v, r, s);
    }
}
