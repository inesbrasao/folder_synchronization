from unittest.mock import Mock
from sync import sync_dirs_by_hashmap

def test_sync_dirs_by_hashmap_synchronized_folders():
    source_path = '/source'
    replica_path = '/replica'
    source_hashmap = {'file1': 'hash1', 'file2': 'hash2'}
    replica_hashmap = {'file1': 'hash1', 'file2': 'hash2'}

    mock_remove = Mock()
    mock_copy = Mock()

    sync_dirs_by_hashmap(
        source_path,
        replica_path,
        source_hashmap,
        replica_hashmap,
        remove_function=mock_remove,
        add_or_copy_function=mock_copy,
    )

    mock_remove.assert_not_called()
    mock_copy.assert_not_called()

def test_sync_dirs_by_hashmap_file_added():
    source_path = '/source'
    replica_path = '/replica'
    source_hashmap = {'file1': 'hash1', 'file2': 'hash2', 'file3': 'hash3'}
    replica_hashmap = {'file1': 'hash1', 'file2': 'hash2'}

    mock_remove = Mock()
    mock_copy = Mock()

    sync_dirs_by_hashmap(
        source_path,
        replica_path,
        source_hashmap,
        replica_hashmap,
        remove_function=mock_remove,
        add_or_copy_function=mock_copy,
    )

    mock_remove.assert_not_called()
    mock_copy.assert_called_once_with('/source/file3', '/replica/file3')

def test_sync_dirs_by_hashmap_file_removed():
    source_path = '/source'
    replica_path = '/replica'
    source_hashmap = {'file1': 'hash1'}
    replica_hashmap = {'file1': 'hash1', 'file2': 'hash2'}

    mock_remove = Mock()
    mock_copy = Mock()

    sync_dirs_by_hashmap(
        source_path,
        replica_path,
        source_hashmap,
        replica_hashmap,
        remove_function=mock_remove,
        add_or_copy_function=mock_copy,
    )

    mock_remove.assert_called_once_with('/replica/file2')
    mock_copy.assert_not_called()

def test_sync_dirs_by_hashmap_file_updated():
    source_path = '/source'
    replica_path = '/replica'
    source_hashmap = {'file1': 'hash1', 'file2': 'new_hash2'}
    replica_hashmap = {'file1': 'hash1', 'file2': 'old_hash2'}

    mock_remove = Mock()
    mock_copy = Mock()

    sync_dirs_by_hashmap(
        source_path,
        replica_path,
        source_hashmap,
        replica_hashmap,
        remove_function=mock_remove,
        add_or_copy_function=mock_copy,
    )

    mock_remove.assert_not_called()
    mock_copy.assert_called_once_with('/source/file2', '/replica/file2')

def test_sync_dirs_by_hashmap_multiple_operations():
    source_path = '/source'
    replica_path = '/replica'
    source_hashmap = {'file1': 'hash1', 'file3': 'hash3'}
    replica_hashmap = {'file1': 'hash1', 'file2': 'hash2'}

    mock_remove = Mock()
    mock_copy = Mock()

    sync_dirs_by_hashmap(
        source_path,
        replica_path,
        source_hashmap,
        replica_hashmap,
        remove_function=mock_remove,
        add_or_copy_function=mock_copy,
    )

    mock_remove.assert_called_once_with('/replica/file2')
    mock_copy.assert_called_once_with('/source/file3', '/replica/file3')

def test_sync_dirs_by_hashmap_empty_directories():
    source_path = '/source'
    replica_path = '/replica'
    source_hashmap = {}
    replica_hashmap = {}

    mock_remove = Mock()
    mock_copy = Mock()

    sync_dirs_by_hashmap(
        source_path,
        replica_path,
        source_hashmap,
        replica_hashmap,
        remove_function=mock_remove,
        add_or_copy_function=mock_copy,
    )

    mock_remove.assert_not_called()
    mock_copy.assert_not_called()